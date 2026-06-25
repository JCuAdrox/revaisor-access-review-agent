# Mathematical-Engineer-Test-AI-Agents

Welcome to the RevAIsor technical test. Your task is to build a tool-augmented AI agent that helps security teams navigate access policies. The code in this repo is your starting point — read the comments and TODOs in each file carefully before you begin.

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
python agent.py "What role does Priya own?"
python agent.py "What is the difference between GBR and ZGBR?"
python agent.py "Show me Priya's access review history."
python agent.py "Order a pizza for the office"
```

## Files

| File | Your Task |
|---|---|
| `knowledge_graph.py` | Complete the KG data |
| `tools.py` | Implement all 5 query functions |
| `agent.py` | Define tools, build the agent loop |
| `evaluator.py` | Bonus — implement the judge |

## Submission

Include a brief write-up explaining:
- Your Knowledge Graph schema
- Your system prompt design
- How `verify_response` prevents hallucinations
- Any trade-offs you made
