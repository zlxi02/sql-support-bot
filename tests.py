"""
Test case definitions for SQL Support Bot evaluation.

55 comprehensive test cases across 8 categories:
- Music Agent: 30 tests (55%)
- Customer Agent: 20 tests (36%)
- General Agent: 5 tests (9%)

To modify tests during interview: Edit this file and re-run Cell 3 in evals.ipynb
"""

from langchain_core.messages import HumanMessage

# ============================================================================
# A. HAPPY PATH - Core Functionality (12 tests)
# ============================================================================
# Goal: Verify all basic features work perfectly
# Coverage: Music (7 tests), Customer (3 tests), General (2 tests)
# ============================================================================

happy_path_tests = [
    
    # ------------------------------------------------------------------------
    # A1. Music/Songs (3 tests) - Basic artist song searches
    # ------------------------------------------------------------------------
    {
        "inputs": {"messages": [HumanMessage(content="Find songs by U2")]},
        "outputs": {
            "test_id": "A1.1",
            "category": "happy_path",
            "subcategory": "music_songs",
            "expected_agent": "music",
            "expected_tool": "get_tracks_by_artist",
            "expected_params": {"artist": "U2"},
            "description": "Basic artist song search - most common music query"
        }
    },
    {
        "inputs": {"messages": [HumanMessage(content="What songs does AC/DC have?")]},
        "outputs": {
            "test_id": "A1.2",
            "category": "happy_path",
            "subcategory": "music_songs",
            "expected_agent": "music",
            "expected_tool": "get_tracks_by_artist",
            "expected_params": {"artist": "AC/DC"},
            "description": "Natural language variation with special characters"
        }
    },
    {
        "inputs": {"messages": [HumanMessage(content="Show me tracks by Metallica")]},
        "outputs": {
            "test_id": "A1.3",
            "category": "happy_path",
            "subcategory": "music_songs",
            "expected_agent": "music",
            "expected_tool": "get_tracks_by_artist",
            "description": "Tests 'tracks' as synonym for songs"
        }
    },
    
    # ------------------------------------------------------------------------
    # A2. Music/Albums (2 tests) - Album-specific queries
    # CRITICAL: Must distinguish "albums" from "songs"
    # ------------------------------------------------------------------------
    {
        "inputs": {"messages": [HumanMessage(content="What albums does Iron Maiden have?")]},
        "outputs": {
            "test_id": "A2.1",
            "category": "happy_path",
            "subcategory": "music_albums",
            "expected_agent": "music",
            "expected_tool": "get_albums_by_artist",
            "expected_params": {"artist": "Iron Maiden"},
            "description": "Album-specific query - critical distinction from songs"
        }
    },
    {
        "inputs": {"messages": [HumanMessage(content="Show me albums by Led Zeppelin")]},
        "outputs": {
            "test_id": "A2.2",
            "category": "happy_path",
            "subcategory": "music_albums",
            "expected_agent": "music",
            "expected_tool": "get_albums_by_artist",
            "description": "Different phrasing for albums"
        }
    },
    
    # ------------------------------------------------------------------------
    # A3. Music/Song Lookup (1 test) - Search by song name (not artist)
    # ------------------------------------------------------------------------
    {
        "inputs": {"messages": [HumanMessage(content="Do you have the song 'One'?")]},
        "outputs": {
            "test_id": "A3.1",
            "category": "happy_path",
            "subcategory": "music_song_lookup",
            "expected_agent": "music",
            "expected_tool": "check_for_songs",
            "expected_params": {"song_title": "One"},
            "description": "Song existence check by name, not artist"
        }
    },
    
    # ------------------------------------------------------------------------
    # A4. Music/Generic (1 test) - Generic "music" query behavior
    # ------------------------------------------------------------------------
    {
        "inputs": {"messages": [HumanMessage(content="Music by Aerosmith")]},
        "outputs": {
            "test_id": "A1.4",
            "category": "happy_path",
            "subcategory": "music_songs",
            "expected_agent": "music",
            "expected_tool": "get_tracks_by_artist",
            "description": "Generic 'music' keyword defaults to songs"
        }
    },
    
    # ------------------------------------------------------------------------
    # A5. Customer (3 tests) - Customer information lookups
    # ------------------------------------------------------------------------
    {
        "inputs": {"messages": [HumanMessage(content="I'm customer 5, what's my email?")]},
        "outputs": {
            "test_id": "A4.1",
            "category": "happy_path",
            "subcategory": "customer",
            "expected_agent": "customer",
            "expected_tool": "get_customer_info",
            "expected_params": {"customer_id": 5},
            "description": "Customer lookup with ID provided - happy path"
        }
    },
    {
        "inputs": {"messages": [HumanMessage(content="Look up customer 10")]},
        "outputs": {
            "test_id": "A4.2",
            "category": "happy_path",
            "subcategory": "customer",
            "expected_agent": "customer",
            "expected_tool": "get_customer_info",
            "expected_params": {"customer_id": 10},
            "description": "Direct customer lookup command"
        }
    },
    {
        "inputs": {"messages": [HumanMessage(content="Customer 15's information please")]},
        "outputs": {
            "test_id": "A4.3",
            "category": "happy_path",
            "subcategory": "customer",
            "expected_agent": "customer",
            "expected_tool": "get_customer_info",
            "expected_params": {"customer_id": 15},
            "description": "Polite customer info request"
        }
    },
    
    # ------------------------------------------------------------------------
    # A6. General (2 tests) - Non-task interactions
    # ------------------------------------------------------------------------
    {
        "inputs": {"messages": [HumanMessage(content="Hello")]},
        "outputs": {
            "test_id": "A5.1",
            "category": "happy_path",
            "subcategory": "general",
            "expected_agent": "general",
            "should_respond_directly": True,
            "description": "Simple greeting - no routing needed"
        }
    },
    {
        "inputs": {"messages": [HumanMessage(content="What can you help me with?")]},
        "outputs": {
            "test_id": "A5.2",
            "category": "happy_path",
            "subcategory": "general",
            "expected_agent": "general",
            "should_respond_directly": True,
            "should_mention_capabilities": True,
            "description": "Capabilities question"
        }
    },
]

# ============================================================================
# B. ROUTING ACCURACY (8 tests)
# ============================================================================
# Goal: Verify queries route to correct agent based on intent
# Coverage: Music routing (3), Customer routing (3), Out-of-scope (2)
# ============================================================================

routing_tests = [
    
    # ------------------------------------------------------------------------
    # B1. Music Routing (3 tests) - Keyword and contextual music routing
    # ------------------------------------------------------------------------
    {
        "inputs": {"messages": [HumanMessage(content="I want to find some rock songs")]},
        "outputs": {
            "test_id": "B1.1",
            "category": "routing",
            "subcategory": "music_routing",
            "expected_agent": "music",
            "routing_keywords": ["songs"],
            "description": "Music keyword 'songs' triggers routing"
        }
    },
    {
        "inputs": {"messages": [HumanMessage(content="What do you have by The Beatles?")]},
        "outputs": {
            "test_id": "B1.2",
            "category": "routing",
            "subcategory": "music_routing",
            "expected_agent": "music",
            "description": "Contextual music query without explicit keyword"
        }
    },
    {
        "inputs": {"messages": [HumanMessage(content="I'm looking for some albums")]},
        "outputs": {
            "test_id": "B1.3",
            "category": "routing",
            "subcategory": "music_routing",
            "expected_agent": "music",
            "routing_keywords": ["albums"],
            "description": "Albums keyword routing"
        }
    },
    
    # ------------------------------------------------------------------------
    # B2. Customer Routing (3 tests) - Customer-related keyword routing
    # ------------------------------------------------------------------------
    {
        "inputs": {"messages": [HumanMessage(content="What's in my account?")]},
        "outputs": {
            "test_id": "B2.1",
            "category": "routing",
            "subcategory": "customer_routing",
            "expected_agent": "customer",
            "routing_keywords": ["account"],
            "description": "Account keyword triggers customer routing"
        }
    },
    {
        "inputs": {"messages": [HumanMessage(content="I need to check my profile")]},
        "outputs": {
            "test_id": "B2.2",
            "category": "routing",
            "subcategory": "customer_routing",
            "expected_agent": "customer",
            "routing_keywords": ["profile"],
            "description": "Profile keyword routing"
        }
    },
    {
        "inputs": {"messages": [HumanMessage(content="Can I see my customer information?")]},
        "outputs": {
            "test_id": "B2.3",
            "category": "routing",
            "subcategory": "customer_routing",
            "expected_agent": "customer",
            "routing_keywords": ["customer", "information"],
            "description": "Customer information lookup"
        }
    },
    
    # ------------------------------------------------------------------------
    # B3. Out-of-Scope (2 tests) - Queries outside agent capabilities
    # ------------------------------------------------------------------------
    {
        "inputs": {"messages": [HumanMessage(content="What are your business hours?")]},
        "outputs": {
            "test_id": "B3.1",
            "category": "routing",
            "subcategory": "out_of_scope",
            "expected_agent": "general",
            "should_not_route": True,
            "description": "Out-of-scope query should not route"
        }
    },
    {
        "inputs": {"messages": [HumanMessage(content="How do I return a purchase?")]},
        "outputs": {
            "test_id": "B3.2",
            "category": "routing",
            "subcategory": "out_of_scope",
            "expected_agent": "general",
            "should_explain_limitations": True,
            "description": "Return policy - out of scope"
        }
    },
]

# ============================================================================
# C. TOOL SELECTION (10 tests) ⭐ MOST CRITICAL CATEGORY
# ============================================================================
# Goal: Verify the RIGHT tool is called for each query type
# Coverage: Albums vs Songs (4), Artist vs Song Name (3), Efficiency (1), Customer (2)
# Why Critical: Prompt changes directly affect tool selection accuracy
# ============================================================================

tool_selection_tests = [
    
    # ------------------------------------------------------------------------
    # C1. Albums vs Songs (4 tests) - ⭐ MOST CRITICAL DISTINCTION
    # Must correctly distinguish between "albums" and "songs/tracks" keywords
    # ------------------------------------------------------------------------
    {
        "inputs": {"messages": [HumanMessage(content="What albums does U2 have?")]},
        "outputs": {
            "test_id": "C1.1",
            "category": "tool_selection",
            "subcategory": "albums_vs_songs",
            "expected_agent": "music",
            "expected_tool": "get_albums_by_artist",
            "should_NOT_call": "get_tracks_by_artist",
            "description": "CRITICAL: 'albums' must use get_albums_by_artist"
        }
    },
    {
        "inputs": {"messages": [HumanMessage(content="What songs does U2 have?")]},
        "outputs": {
            "test_id": "C1.2",
            "category": "tool_selection",
            "subcategory": "albums_vs_songs",
            "expected_agent": "music",
            "expected_tool": "get_tracks_by_artist",
            "should_NOT_call": "get_albums_by_artist",
            "description": "CRITICAL: 'songs' must use get_tracks_by_artist"
        }
    },
    {
        "inputs": {"messages": [HumanMessage(content="Show me tracks by Iron Maiden")]},
        "outputs": {
            "test_id": "C1.3",
            "category": "tool_selection",
            "subcategory": "albums_vs_songs",
            "expected_agent": "music",
            "expected_tool": "get_tracks_by_artist",
            "description": "'tracks' is synonym for songs"
        }
    },
    {
        "inputs": {"messages": [HumanMessage(content="What records does Pink Floyd have?")]},
        "outputs": {
            "test_id": "C1.4",
            "category": "tool_selection",
            "subcategory": "albums_vs_songs",
            "expected_agent": "music",
            "expected_tool": "get_albums_by_artist",
            "description": "'records' is synonym for albums"
        }
    },
    
    # ------------------------------------------------------------------------
    # C2. Artist Lookup vs Song Name Lookup (3 tests)
    # Distinguish between searching by artist name vs searching for song title
    # ------------------------------------------------------------------------
    {
        "inputs": {"messages": [HumanMessage(content="Find music by Metallica")]},
        "outputs": {
            "test_id": "C2.1",
            "category": "tool_selection",
            "subcategory": "artist_vs_song_name",
            "expected_agent": "music",
            "expected_tool": "get_tracks_by_artist",
            "expected_params": {"artist": "Metallica"},
            "description": "By artist name uses get_tracks_by_artist"
        }
    },
    {
        "inputs": {"messages": [HumanMessage(content="Do you have 'Bohemian Rhapsody'?")]},
        "outputs": {
            "test_id": "C2.2",
            "category": "tool_selection",
            "subcategory": "artist_vs_song_name",
            "expected_agent": "music",
            "expected_tool": "check_for_songs",
            "expected_params": {"song_title": "Bohemian Rhapsody"},
            "should_NOT_call": "get_tracks_by_artist",
            "description": "CRITICAL: Song name uses check_for_songs"
        }
    },
    {
        "inputs": {"messages": [HumanMessage(content="Find the song 'Beautiful Day'")]},
        "outputs": {
            "test_id": "C2.3",
            "category": "tool_selection",
            "subcategory": "artist_vs_song_name",
            "expected_agent": "music",
            "expected_tool": "check_for_songs",
            "description": "Song title with quotes uses check_for_songs"
        }
    },
    
    # ------------------------------------------------------------------------
    # C3. Tool Efficiency (1 test) - Avoid unnecessary tool calls
    # ------------------------------------------------------------------------
    {
        "inputs": {"messages": [HumanMessage(content="Do you have 'One' by U2?")]},
        "outputs": {
            "test_id": "C3.1",
            "category": "tool_selection",
            "subcategory": "tool_efficiency",
            "expected_agent": "music",
            "expected_tool": "check_for_songs",
            "description": "Should only call check_for_songs, not other tools"
        }
    },
    
    # ------------------------------------------------------------------------
    # C4. Customer Tool (2 tests) - Customer lookup parameter extraction
    # ------------------------------------------------------------------------
    {
        "inputs": {"messages": [HumanMessage(content="Look up customer 20")]},
        "outputs": {
            "test_id": "C4.1",
            "category": "tool_selection",
            "subcategory": "customer_tool",
            "expected_agent": "customer",
            "expected_tool": "get_customer_info",
            "expected_params": {"customer_id": 20},
            "description": "Customer lookup with correct parameter"
        }
    },
    {
        "inputs": {"messages": [HumanMessage(content="Get info for customer 25")]},
        "outputs": {
            "test_id": "C4.2",
            "category": "tool_selection",
            "subcategory": "customer_tool",
            "expected_agent": "customer",
            "expected_tool": "get_customer_info",
            "expected_params": {"customer_id": 25},
            "description": "Alternate phrasing for customer lookup"
        }
    },
]

# ============================================================================
# D. PARAMETER EXTRACTION (5 tests)
# ============================================================================
# Goal: Verify correct entity extraction from natural language queries
# Coverage: Artist names (3 tests), Customer IDs (2 tests)
# ============================================================================

parameter_tests = [
    
    # ------------------------------------------------------------------------
    # D1. Artist Extraction (3 tests) - Extract artist names from queries
    # Tests: simple names, multi-word names, special characters
    # ------------------------------------------------------------------------
    {
        "inputs": {"messages": [HumanMessage(content="Songs by Madonna")]},
        "outputs": {
            "test_id": "D1.1",
            "category": "parameter_extraction",
            "subcategory": "artist_extraction",
            "expected_agent": "music",
            "extracted_artist": "Madonna",
            "description": "Simple artist name extraction"
        }
    },
    {
        "inputs": {"messages": [HumanMessage(content="Albums by Iron Maiden")]},
        "outputs": {
            "test_id": "D1.2",
            "category": "parameter_extraction",
            "subcategory": "artist_extraction",
            "expected_agent": "music",
            "extracted_artist": "Iron Maiden",
            "description": "Multi-word artist name extraction"
        }
    },
    {
        "inputs": {"messages": [HumanMessage(content="Music by AC/DC")]},
        "outputs": {
            "test_id": "D1.3",
            "category": "parameter_extraction",
            "subcategory": "artist_extraction",
            "expected_agent": "music",
            "extracted_artist": "AC/DC",
            "description": "Artist with special characters (slash)"
        }
    },
    
    # ------------------------------------------------------------------------
    # D2. Customer ID Extraction (2 tests) - Extract numeric IDs from text
    # ------------------------------------------------------------------------
    {
        "inputs": {"messages": [HumanMessage(content="I'm customer number 42")]},
        "outputs": {
            "test_id": "D2.1",
            "category": "parameter_extraction",
            "subcategory": "customer_id_extraction",
            "expected_agent": "customer",
            "extracted_customer_id": 42,
            "description": "Customer ID from natural language"
        }
    },
    {
        "inputs": {"messages": [HumanMessage(content="Customer ID: 30")]},
        "outputs": {
            "test_id": "D2.2",
            "category": "parameter_extraction",
            "subcategory": "customer_id_extraction",
            "expected_agent": "customer",
            "extracted_customer_id": 30,
            "description": "Customer ID with colon format"
        }
    },
]

# ============================================================================
# E. DATA HANDLING (6 tests)
# ============================================================================
# Goal: Handle real database scenarios (existing data, missing data, typos)
# Coverage: Music (3 tests), Customer (3 tests)
# ============================================================================

data_handling_tests = [
    
    # ------------------------------------------------------------------------
    # E1. Existing Data (2 tests) - Queries that should return results
    # ------------------------------------------------------------------------
    {
        "inputs": {"messages": [HumanMessage(content="Songs by U2")]},
        "outputs": {
            "test_id": "E1.1",
            "category": "data_handling",
            "subcategory": "existing_data",
            "expected_agent": "music",
            "artist_exists": True,
            "should_return_results": True,
            "description": "Common artist - should return many results"
        }
    },
    
    # ------------------------------------------------------------------------
    # E2. Nonexistent Data (2 tests) - Graceful handling of missing data
    # ------------------------------------------------------------------------
    {
        "inputs": {"messages": [HumanMessage(content="Songs by Taylor Swift")]},
        "outputs": {
            "test_id": "E2.1",
            "category": "data_handling",
            "subcategory": "nonexistent_data",
            "expected_agent": "music",
            "artist_exists": False,
            "should_handle_gracefully": True,
            "description": "Nonexistent artist - graceful failure"
        }
    },
    {
        "inputs": {"messages": [HumanMessage(content="Look up customer 99999")]},
        "outputs": {
            "test_id": "E2.2",
            "category": "data_handling",
            "subcategory": "nonexistent_data",
            "expected_agent": "customer",
            "customer_exists": False,
            "should_handle_gracefully": True,
            "description": "Nonexistent customer ID"
        }
    },
    
    # ------------------------------------------------------------------------
    # E3. Fuzzy Matching & Edge Cases (2 tests) - Typos and boundary data
    # ------------------------------------------------------------------------
    {
        "inputs": {"messages": [HumanMessage(content="Songs by Beetles")]},
        "outputs": {
            "test_id": "E3.1",
            "category": "data_handling",
            "subcategory": "fuzzy_matching",
            "expected_agent": "music",
            "typo_in_query": True,
            "should_fuzzy_match": "The Beatles",
            "description": "Typo should fuzzy match via LIKE"
        }
    },
    {
        "inputs": {"messages": [HumanMessage(content="Look up customer 1")]},
        "outputs": {
            "test_id": "E1.2",
            "category": "data_handling",
            "subcategory": "existing_data",
            "expected_agent": "customer",
            "customer_exists": True,
            "should_return_info": True,
            "description": "Existing customer lookup"
        }
    },
    {
        "inputs": {"messages": [HumanMessage(content="Customer 59 information")]},
        "outputs": {
            "test_id": "E3.2",
            "category": "data_handling",
            "subcategory": "edge_data",
            "expected_agent": "customer",
            "customer_id": 59,
            "description": "Edge case - last valid customer ID in database"
        }
    },
]

# ============================================================================
# F. EDGE CASES (5 tests)
# ============================================================================
# Goal: Test unusual inputs and boundary conditions
# Coverage: Music (2), Customer (2), General (1)
# ============================================================================

edge_case_tests = [
    
    # ------------------------------------------------------------------------
    # F1. Verbose & Case Handling - Music (2 tests)
    # ------------------------------------------------------------------------
    {
        "inputs": {"messages": [HumanMessage(content="Hi I'm looking for music and I was wondering if you could help me find songs by U2")]},
        "outputs": {
            "test_id": "F1.1",
            "category": "edge_cases",
            "subcategory": "verbose_input",
            "expected_agent": "music",
            "extracted_artist": "U2",
            "description": "Very long verbose query"
        }
    },
    {
        "inputs": {"messages": [HumanMessage(content="SONGS BY U2")]},
        "outputs": {
            "test_id": "F2.1",
            "category": "edge_cases",
            "subcategory": "case_handling",
            "expected_agent": "music",
            "case_insensitive": True,
            "description": "All caps input"
        }
    },
    
    # ------------------------------------------------------------------------
    # F2. Case Handling - Customer (2 tests)
    # ------------------------------------------------------------------------
    {
        "inputs": {"messages": [HumanMessage(content="CUSTOMER 10 EMAIL")]},
        "outputs": {
            "test_id": "F3.1",
            "category": "edge_cases",
            "subcategory": "case_handling",
            "expected_agent": "customer",
            "extracted_customer_id": 10,
            "description": "All caps customer query"
        }
    },
    {
        "inputs": {"messages": [HumanMessage(content="im customer 7 what's my info")]},
        "outputs": {
            "test_id": "F4.1",
            "category": "edge_cases",
            "subcategory": "case_handling",
            "expected_agent": "customer",
            "all_lowercase": True,
            "description": "All lowercase with no punctuation"
        }
    },
    
    # ------------------------------------------------------------------------
    # F3. Gibberish Input - General (1 test)
    # ------------------------------------------------------------------------
    {
        "inputs": {"messages": [HumanMessage(content="asdfghjkl")]},
        "outputs": {
            "test_id": "F5.1",
            "category": "edge_cases",
            "subcategory": "gibberish",
            "expected_agent": "general",
            "should_not_crash": True,
            "description": "Gibberish input"
        }
    },
]

# ============================================================================
# G. ERROR HANDLING & BOUNDARIES (4 tests)
# ============================================================================
# Goal: Test capability limits and error scenarios
# Coverage: Music (1), Customer (3)
# ============================================================================

error_handling_tests = [
    
    # ------------------------------------------------------------------------
    # G1. Out of Capability - Music (1 test)
    # ------------------------------------------------------------------------
    {
        "inputs": {"messages": [HumanMessage(content="Delete all songs by U2")]},
        "outputs": {
            "test_id": "G1.1",
            "category": "error_handling",
            "subcategory": "out_of_capability",
            "expected_agent": "music",
            "should_explain_cannot_do": True,
            "description": "Delete request - out of capability"
        }
    },
    
    # ------------------------------------------------------------------------
    # G2. Capability Boundaries - Customer (3 tests)
    # CRITICAL: Tests that agent explains limitations (can only lookup, not update/delete)
    # ------------------------------------------------------------------------
    {
        "inputs": {"messages": [HumanMessage(content="Update my email to newemail@example.com")]},
        "outputs": {
            "test_id": "G2.1",
            "category": "error_handling",
            "subcategory": "capability_boundary",
            "expected_agent": "customer",
            "should_explain_limitation": True,
            "should_mention_lookup_only": True,
            "description": "CRITICAL: Update request - can only lookup, not update"
        }
    },
    {
        "inputs": {"messages": [HumanMessage(content="Delete my account")]},
        "outputs": {
            "test_id": "G3.1",
            "category": "error_handling",
            "subcategory": "capability_boundary",
            "expected_agent": "customer",
            "should_explain_cannot_do": True,
            "description": "Delete request - out of capability"
        }
    },
    {
        "inputs": {"messages": [HumanMessage(content="Look up customer -5")]},
        "outputs": {
            "test_id": "G4.1",
            "category": "error_handling",
            "subcategory": "invalid_input",
            "expected_agent": "customer",
            "invalid_customer_id": True,
            "should_handle_gracefully": True,
            "description": "Negative customer ID"
        }
    },
]

# ============================================================================
# H. MULTI-TURN CONVERSATIONS (6 tests)
# ============================================================================
# Goal: Test context retention and conversation flow
# Coverage: Music (4), Customer (2)
# Note: Multi-turn evaluation requires more complex setup
# ============================================================================

multi_turn_tests = [
    
    # ------------------------------------------------------------------------
    # H1. Music Conversations (4 tests) - Follow-ups and multi-request queries
    # ------------------------------------------------------------------------
    {
        "inputs": {"messages": [HumanMessage(content="I'm looking for music")]},
        "outputs": {
            "test_id": "H1.1",
            "category": "multi_turn",
            "subcategory": "music_conversation",
            "expected_agent": "music",
            "should_ask_for_artist": True,
            "description": "Multi-turn: User asks for music, agent should ask which artist"
        }
    },
    {
        "inputs": {"messages": [HumanMessage(content="What albums does U2 have?")]},
        "outputs": {
            "test_id": "H1.2",
            "category": "multi_turn",
            "subcategory": "music_conversation_setup",
            "expected_agent": "music",
            "expected_tool": "get_albums_by_artist",
            "description": "Multi-turn setup: Get albums first (for follow-up query test)"
        }
    },
    {
        "inputs": {"messages": [HumanMessage(content="Show me both albums and songs by Aerosmith")]},
        "outputs": {
            "test_id": "H1.3",
            "category": "multi_turn",
            "subcategory": "music_multi_request",
            "expected_agent": "music",
            "requires_multiple_tools": True,
            "description": "Request for both albums and songs"
        }
    },
    {
        "inputs": {"messages": [HumanMessage(content="Get albums by Led Zeppelin and then get their tracks")]},
        "outputs": {
            "test_id": "H1.4",
            "category": "multi_turn",
            "subcategory": "music_sequential_tools",
            "expected_agent": "music",
            "expected_tools_called": ["get_albums_by_artist", "get_tracks_by_artist"],
            "check_tool_order": False,  # Order doesn't matter - both should be called
            "expected_params": {"artist": "Led Zeppelin"},
            "response_should_contain": ["album", "track"],
            "description": "MULTI-TOOL: Validates agent calls multiple tools sequentially for comprehensive music query"
        }
    },
    
    # ------------------------------------------------------------------------
    # H2. Customer Conversations (2 tests) - Missing ID follow-up flows
    # IMPORTANT: Agent should ask for customer ID when not provided
    # ------------------------------------------------------------------------
    {
        "inputs": {"messages": [HumanMessage(content="What's my email?")]},
        "outputs": {
            "test_id": "H2.1",
            "category": "multi_turn",
            "subcategory": "customer_conversation",
            "expected_agent": "customer",
            "should_ask_for_id": True,
            "description": "IMPORTANT: Customer asks without ID, agent should ask for it"
        }
    },
    {
        "inputs": {"messages": [HumanMessage(content="I need help with my account")]},
        "outputs": {
            "test_id": "H2.2",
            "category": "multi_turn",
            "subcategory": "customer_conversation",
            "expected_agent": "customer",
            "should_ask_for_id": True,
            "description": "Account help request - should ask for ID"
        }
    },
]

# ============================================================================
# COMBINE ALL TESTS
# ============================================================================

all_tests = (
    happy_path_tests +
    routing_tests +
    tool_selection_tests +
    parameter_tests +
    data_handling_tests +
    edge_case_tests +
    error_handling_tests +
    multi_turn_tests
)

# ============================================================================
# SUMMARY INFO
# ============================================================================

TEST_SUMMARY = {
    "total": len(all_tests),
    "by_category": {
        "happy_path": len(happy_path_tests),
        "routing": len(routing_tests),
        "tool_selection": len(tool_selection_tests),
        "parameter_extraction": len(parameter_tests),
        "data_handling": len(data_handling_tests),
        "edge_cases": len(edge_case_tests),
        "error_handling": len(error_handling_tests),
        "multi_turn": len(multi_turn_tests),
    },
    "by_agent": {
        "music": sum(1 for t in all_tests if t["outputs"].get("expected_agent") == "music"),
        "customer": sum(1 for t in all_tests if t["outputs"].get("expected_agent") == "customer"),
        "general": sum(1 for t in all_tests if t["outputs"].get("expected_agent") == "general"),
    }
}

