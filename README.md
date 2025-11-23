# Zachary Xi - SQL Support Bot Eval Framework

Hi Harrison and Sam, thanks for taking the time to review my take home!

**Recommended Review Order:**
1. Open `EVALUATION_FRAMEWORK.html` in browser -- overview of the evaluation framework
2. Open `TEST_SUMMARY.html` in browser -- deep dive into the test cases
3. Review `evals.ipynb` (eval framework) and `agent_config.py` (rapid iteration config)

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
