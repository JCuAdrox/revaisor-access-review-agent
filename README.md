# RevAIsor Access Review Agent

## Setup

```
pip install -r requirements.txt
pip install google-genai
```

This project uses the unified Google GenAI SDK (google-genai, imported as "from google import genai"), not the legacy google-generativeai package originally listed in requirements.txt.

Before running anything, set your own Google API key as an environment variable. This key is never stored anywhere in this repository, so each person running this project needs to set their own, obtained for free from Google AI Studio.

In Git Bash, one line at a time:

```
export GOOGLE_API_KEY="your_own_key_here"
```

## Run

```
python agent.py "What role does Priya own?"
python agent.py "What is the difference between GBR and ZGBR?"
python agent.py "Show me Priya's access review history."
python agent.py "Order a pizza for the office"
```

The evaluator (bonus, external LLM judge) can be run the same way:

```
python evaluator.py "What role does Priya own?"
```

## Files

knowledge_graph.py holds the static Knowledge Graph.
tools.py holds role_tool and document_tool, already implemented.
router.py routes a query to an intent and the tools to call.
agent.py runs the main agent loop and the rule based verifier.
evaluator.py holds the bonus, an independent LLM judge.

## Design Notes

### 1. Knowledge Graph Schema

knowledge_graph.py defines one dictionary, KG, with three connected sections implementing the required Role to Ownership Role to GBR/ZGBR hierarchy.

role_types holds the two role type nodes, GBR and ZGBR, each with its properties (access_model, session_verification, description) and a differs_from field pointing to its counterpart. This is the contrastive edge the assignment asks for. It tells the agent explicitly that GBR and ZGBR are meant to be compared, so comparison questions can be answered from the graph itself instead of being inferred or hallucinated.

documents holds policy fragments, each with a source_id for mandatory citation, mirroring what document_tool returns.

users holds role ownership per user (owns, role_type, department, review_history), mirroring what role_tool returns.

We used a plain nested dictionary rather than networkx. For a graph this small (2 role types, 3 users, 3 documents) a graph library adds overhead without adding expressive power, and the assignment explicitly allows a dictionary. tools.py simulates an external system of record; KG is the agent's own internal reasoning map, consulted before any tool call.

### 2. Routing Strategy

router.py is deterministic, with no LLM involved, and runs in three steps.

extract_entities does a case insensitive substring match against the known users and role types in KG. The graph is the source of truth for what counts as a recognized entity.

classify_intent does keyword matching, checked in a deliberate priority order. Comparison is checked first, so a query mentioning both a role type and comparison words like "difference" or "vs" isn't misread as plain ownership. Then access history, then role ownership, then an entity based fallback for unmatched phrasing, and finally out of scope by default.

select_tools maps intent directly to the tool or tools to call.

out_of_scope is entity driven rather than keyword blocklist driven, on purpose. A blocklist can never anticipate every irrelevant phrasing. Falling back to out_of_scope whenever no known entity is found is far more robust, since it doesn't depend on predicting how someone might phrase an off topic request.

### 3. How the Verifier Prevents Hallucinations

Two independent safety layers are kept deliberately separate.

verify_response, inside agent.py, is rule based, makes no LLM call, and runs on every single query. It checks that the answer cites a known source_id or Role DB, and that any role ID shaped token in the answer (such as GBR 1234) actually exists in KG users, flagging anything that doesn't as a possible invented ID. Out of scope refusals are exempted from the citation check, since they make no factual claim.

evaluate, inside evaluator.py, is the bonus. It is a fully independent LLM call that does not reuse the agent's own reasoning, and audits grounding, citation accuracy, and relevance given only the query, the raw tool output, and the agent's final answer.

Both layers were refined after catching real false positives during testing. verify_response initially matched role ID shaped fragments inside citations themselves, for example GBR 001 inside Policy Doc GBR 001, and flagged them as invented. The fix strips known source_ids from the text before checking for invented role IDs. Separately, the LLM judge in evaluate initially marked a correct out of scope refusal as not relevant, because nothing was retrieved. The fix was to clarify in the judge's own prompt that a correct refusal to an out of scope query is relevant, and that empty tool output should default grounding and citation checks to pass rather than fail.

### 4. Key Trade offs

Role and document data is duplicated between tools.py, which simulates an external system of record, and knowledge_graph.py, the internal reasoning map. At production scale the KG would need to sync from the source system instead of being hand maintained.

Intent classification is keyword based rather than LLM based. This is fully explainable and deterministic as required, but less flexible for unanticipated phrasing.

Both agent.py and evaluator.py call the LLM through a small model fallback list with exponential backoff, since the available model catalog changed (deprecations, temporary overload, and per key permission differences) during development. This reflects a realistic condition for any system that depends on a third party LLM provider.