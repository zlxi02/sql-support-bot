# SQL Support Bot + Evaluation Framework

A multi-agent customer support bot that routes queries to specialized agents (Music, Customer, General) and interacts with a SQL database. Includes a comprehensive evaluation framework with 55 test cases across 8 categories.

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Add your API keys to `.env`:
```
OPENAI_API_KEY=your-key-here
LANGCHAIN_API_KEY=your-key-here
```

## File Structure

### Core Agent
- **`agent.ipynb`** - Original multi-agent chatbot implementation (3 agents: general, music, customer)
- **`agent_config.py`** - Refactored agent configuration (prompts, tools, graph builder) for easy testing

### Evaluation Framework
- **`evals.ipynb`** - Main evaluation notebook (dataset upload, evaluators, baseline testing, comparison tools)
- **`tests.py`** - 55 test case definitions organized by category (Happy Path, Routing, Tool Selection, etc.)
- **`requirements.txt`** - All dependencies including LangSmith integration

### Documentation
- **`EVALUATION_FRAMEWORK.html`** - Complete framework documentation (architecture, components, workflow)
- **`TEST_SUMMARY.html`** - Detailed test case breakdown with examples

## Quick Start

1. **Run the agent:** Open `agent.ipynb` and run cells to test the chatbot interactively
2. **Run evaluations:** Open `evals.ipynb` to upload tests to LangSmith and run baseline evaluation
3. **View results:** Check `EVALUATION_FRAMEWORK.html` for detailed documentation

For full evaluation framework details, see `EVALUATION_FRAMEWORK.html`.
