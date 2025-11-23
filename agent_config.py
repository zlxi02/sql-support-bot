"""
Agent Configuration and Graph Builder

This module provides configurable prompts and a function to build the 
multi-agent SQL support bot graph with different configurations.
"""

import sqlite3
import requests
from functools import partial

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_community.utilities.sql_database import SQLDatabase
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from pydantic import BaseModel, Field

from langgraph.graph import MessageGraph, END
from langgraph.prebuilt import ToolNode


# ============================================================================
# DATABASE SETUP
# ============================================================================

def get_engine_for_chinook_db():
    """Pull sql file, populate in-memory database, and create engine."""
    url = "https://raw.githubusercontent.com/lerocha/chinook-database/master/ChinookDatabase/DataSources/Chinook_Sqlite.sql"
    response = requests.get(url)
    sql_script = response.text

    connection = sqlite3.connect(":memory:", check_same_thread=False)
    connection.executescript(sql_script)
    return create_engine(
        "sqlite://",
        creator=lambda: connection,
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
    )


# ============================================================================
# PROMPTS
# ============================================================================

CUSTOMER_PROMPT = """Your job is to help a user update their profile.

You only have certain tools you can use. These tools require specific input. If you don't know the required input, then ask the user for it.

If you are unable to help the user, you can """

MUSIC_PROMPT = """Your job is to help a customer find any songs they are looking for. 

You only have certain tools you can use. If a customer asks you to look something up that you don't know how, politely tell them what you can help with.

When looking up artists and songs, sometimes the artist/song will not be found. In that case, the tools will return information on simliar songs and artists. This is intentional, it is not the tool messing up."""

GENERAL_PROMPT = """Your job is to help as a customer service representative for a music store.

You should interact politely with customers to try to figure out how you can help. You can help in a few ways:

- Updating user information: if a customer wants to update the information in the user database. Call the router with `customer`
- Recomending music: if a customer wants to find some music or information about music. Call the router with `music`

If the user is asking or wants to ask about updating or accessing their information, send them to that route.
If the user is asking or wants to ask about music, send them to that route.
Otherwise, respond."""

# ============================================================================
# PROMPTS - CURRENT (Edit during interview)
# ============================================================================

CURRENT_CUSTOMER_PROMPT = """Your job is to help a user update their profile.

You only have certain tools you can use. These tools require specific input. If you don't know the required input, then ask the user for it.

If you are unable to help the user, you can """

CURRENT_MUSIC_PROMPT = """Your job is to help a customer find any songs they are looking for.

TOOL SELECTION GUIDE:
- If user asks for 'albums' or 'records' → use get_albums_by_artist
- If user asks for 'songs', 'tracks', or 'music' → use get_tracks_by_artist
- If user asks 'do you have [song name]' → use check_for_songs

When looking up artists and songs, sometimes the artist/song will not be found. In that case, the tools will return information on similar songs and artists. This is intentional, it is not the tool messing up."""

CURRENT_GENERAL_PROMPT = """Your job is to help as a customer service representative for a music store.

You should interact politely with customers to try to figure out how you can help. You can help in a few ways:

- Updating user information: if a customer wants to update the information in the user database. Call the router with `customer`
- Recomending music: if a customer wants to find some music or information about music. Call the router with `music`

If the user is asking or wants to ask about updating or accessing their information, send them to that route.
If the user is asking or wants to ask about music, send them to that route.
Otherwise, respond."""


# ============================================================================
# CONFIGURATIONS
# ============================================================================

CONFIGS = {
    "baseline": {
        "general_prompt": GENERAL_PROMPT,
        "music_prompt": MUSIC_PROMPT,
        "customer_prompt": CUSTOMER_PROMPT,
        "model_name": "gpt-4o",
        "temperature": 0,
        "streaming": False,  # False for faster evals
    },
    "current": {
        # Uses CURRENT_* prompts which you can modify during interview
        "general_prompt": CURRENT_GENERAL_PROMPT,
        "music_prompt": CURRENT_MUSIC_PROMPT,
        "customer_prompt": CURRENT_CUSTOMER_PROMPT,
        "model_name": "gpt-4o",
        "temperature": 0,
        "streaming": False,
    }
}


# ============================================================================
# GRAPH BUILDER
# ============================================================================

def build_graph(config):
    """
    Build the complete multi-agent graph with specified configuration.
    
    Args:
        config: Dictionary with keys:
            - general_prompt: str (router agent prompt)
            - music_prompt: str (music agent prompt)
            - customer_prompt: str (customer agent prompt)
            - model_name: str (e.g., "gpt-4o", "gpt-3.5-turbo")
            - temperature: float (0-1, for response randomness)
            - streaming: bool (whether to stream responses)
    
    Returns:
        Compiled LangGraph workflow
    """
    
    # ========================================================================
    # SETUP: Extract Config & Initialize Core Components
    # ========================================================================
    
    # Extract config parameters
    general_prompt = config["general_prompt"]
    music_prompt = config["music_prompt"]
    customer_prompt = config["customer_prompt"]
    model_name = config["model_name"]
    temperature = config["temperature"]
    streaming = config.get("streaming", False)
    
    # Setup database (from notebook Cell 5)
    engine = get_engine_for_chinook_db()
    db = SQLDatabase(engine)
    
    # Create LLM model (from notebook Cell 8)
    model = ChatOpenAI(
        temperature=temperature,
        streaming=streaming,
        model=model_name
    )
    
    # ========================================================================
    # TOOLS: Define all tools for agents (from notebook Cells 12, 16, 18, 20)
    # ========================================================================
    # NOTE: Tools must be inside function to access 'db'
    # Modify tool docstrings or SQL queries here during interview
    # --- Customer Tool (Cell 12) ---
    @tool
    def get_customer_info(customer_id: int):
        """Look up customer info given their ID. ALWAYS make sure you have the customer ID before invoking this."""
        return db.run(f"SELECT * FROM Customer WHERE CustomerID = {customer_id};")
    
    # --- Music Tools (Cells 16, 18, 20) ---
    @tool
    def get_albums_by_artist(artist: str):
        """Get albums by an artist."""
        return db.run(
            f"""
            SELECT Album.Title, Artist.Name 
            FROM Album 
            JOIN Artist ON Album.ArtistId = Artist.ArtistId 
            WHERE Artist.Name LIKE '%{artist}%';
            """,
            include_columns=True
        )
    
    @tool
    def get_tracks_by_artist(artist: str):
        """Get songs by an artist (or similar artists)."""
        return db.run(
            f"""
            SELECT Track.Name as SongName, Artist.Name as ArtistName 
            FROM Album 
            LEFT JOIN Artist ON Album.ArtistId = Artist.ArtistId 
            LEFT JOIN Track ON Track.AlbumId = Album.AlbumId 
            WHERE Artist.Name LIKE '%{artist}%';
            """,
            include_columns=True
        )
    
    @tool
    def check_for_songs(song_title):
        """Check if a song exists by its name."""
        return db.run(
            f"""
            SELECT * FROM Track WHERE Name LIKE '%{song_title}%';
            """,
            include_columns=True
        )
    
    # --- Router Tool (Cell 25) ---
    class Router(BaseModel):
        """Call this if you are able to route the user to the appropriate representative."""
        choice: str = Field(description="should be one of: music, customer")
    
    # ========================================================================
    # AGENT CHAINS: Build the 3 specialized agents (Cells 13, 22, 26)
    # ========================================================================
    
    # --- Customer Agent Chain (Cell 13) ---
    def get_customer_messages(messages):
        return [SystemMessage(content=customer_prompt)] + messages
    
    customer_chain = get_customer_messages | model.bind_tools([get_customer_info])
    
    # --- Music Agent Chain (Cell 22) ---
    # To modify which tools music agent can use, add/remove from this list
    def get_song_messages(messages):
        return [SystemMessage(content=music_prompt)] + messages
    
    song_recc_chain = get_song_messages | model.bind_tools([
        get_albums_by_artist,
        get_tracks_by_artist,
        check_for_songs
    ])
    
    # --- General/Router Agent Chain (Cell 26) ---
    def get_messages(messages):
        return [SystemMessage(content=general_prompt)] + messages
    
    chain = get_messages | model.bind_tools([Router])
    
    # ========================================================================
    # ROUTING LOGIC: Helper functions for graph navigation (Cells 29, 30)
    # ========================================================================
    # This is the "brain" that decides which agent to use next
    
    def add_name(message, name):
        """Tag messages with agent name for tracking (Cell 29)"""
        _dict = message.model_dump()
        _dict["name"] = name
        return AIMessage(**_dict)
    
    def _get_last_ai_message(messages):
        """Find most recent AI message in conversation"""
        for m in messages[::-1]:
            if isinstance(m, AIMessage):
                return m
        return None
    
    def _is_tool_call(msg):
        """Check if message contains a tool call"""
        return hasattr(msg, "tool_calls") and len(msg.tool_calls) > 0
    
    def _route(messages):
        """
        Routing function - decides which node to visit next (Cell 30)
        Returns: "general", "music", "customer", "tools", or END
        """
        last_message = messages[-1]
        if isinstance(last_message, AIMessage):
            if not _is_tool_call(last_message):
                return END
            else:
                if last_message.name == "general":
                    tool_calls = last_message.tool_calls
                    if len(tool_calls) > 1:
                        raise ValueError("General agent should only call one tool")
                    tool_call = tool_calls[0]
                    return tool_call['args']['choice']
                else:
                    return "tools"
        last_m = _get_last_ai_message(messages)
        if last_m is None:
            return "general"
        if last_m.name == "music":
            return "music"
        elif last_m.name == "customer":
            return "customer"
        else:
            return "general"
    
    def _filter_out_routes(messages):
        """Remove internal Router tool calls from conversation history (Cell 32)"""
        ms = []
        for m in messages:
            if _is_tool_call(m):
                if m.name == "general":
                    continue  # Skip Router calls
            ms.append(m)
        return ms
    
    # ========================================================================
    # NODES: Assemble the graph nodes (Cells 31, 33)
    # ========================================================================
    
    # Tools node - executes all tool calls (Cell 31)
    # To add a new tool, add it to this list
    tools = [get_albums_by_artist, get_tracks_by_artist, check_for_songs, get_customer_info]
    tools_node = ToolNode(tools)
    
    # Agent nodes - each filters routes, runs chain, tags with name (Cell 33)
    general_node = _filter_out_routes | chain | partial(add_name, name="general")
    music_node = _filter_out_routes | song_recc_chain | partial(add_name, name="music")
    customer_node = _filter_out_routes | customer_chain | partial(add_name, name="customer")
    
    # ========================================================================
    # GRAPH ASSEMBLY: Connect all nodes with routing logic (Cell 34)
    # ========================================================================
    
    # Create graph and define node mapping
    workflow = MessageGraph()
    nodes = {"general": "general", "music": "music", END: END, "tools": "tools", "customer": "customer"}
    
    # Add all 4 nodes to the graph
    workflow.add_node("general", general_node)    # Router agent
    workflow.add_node("music", music_node)        # Music specialist
    workflow.add_node("customer", customer_node)  # Customer specialist
    workflow.add_node("tools", tools_node)        # Tool executor
    
    # Add conditional edges - after each node, call _route to decide where to go next
    workflow.add_conditional_edges("general", _route, nodes)
    workflow.add_conditional_edges("tools", _route, nodes)
    workflow.add_conditional_edges("music", _route, nodes)
    workflow.add_conditional_edges("customer", _route, nodes)
    
    # Set entry point - start by calling _route to decide first node
    workflow.set_conditional_entry_point(_route, nodes)
    
    # Compile and return the executable graph
    return workflow.compile()


# ============================================================================
# CONVENIENCE FUNCTION
# ============================================================================

def build_baseline_graph():
    """Quick function to build graph with baseline config."""
    return build_graph(CONFIGS["baseline"])

