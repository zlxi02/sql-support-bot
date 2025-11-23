# Zachary Xi - SQL Support Bot Eval Framework

Hi Harrison and Chase, thanks for taking the time to review my take home. Here's how I would recommend reviewing this:

1. Open HTML file `EVALUATION_FRAMEWORK.html` in a browser tab -- this is a summary of the evaluation framework
2. Open HTML file `TEST_SUMMARY.html` in a browser tab -- this is a deep dive for test cases
3. Review the core agent / eval framework. Most notable files are:
   - `evals.ipynb` - the eval framework
   - `agent_config.py` - quickly make agent changes, created for rapid iteration

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
