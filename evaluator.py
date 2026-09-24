"""
evaluator.py

This component is INDEPENDENT of the agent loop.
It acts as an external judge that critiques the agent's output.

It receives:
  1. The original user query
  2. The raw tool outputs
  3. The agent's final answer

And it returns a score with reasoning on three criteria:
  - GROUNDING  : Did the agent avoid hallucinating data not in the tool output?
  - CITATIONS  : Did the agent correctly map findings to source_ids?
  - RELEVANCE  : Did the agent directly answer the user's question?

Usage:
    python evaluator.py "What role does Priya own?"
"""

from __future__ import annotations

import sys
import json
import os
import logging
import time
# LLM SDKs — choose one
import openai
from google import genai

logging.getLogger("google_genai").setLevel(logging.ERROR)
logging.getLogger("google_genai.models").setLevel(logging.ERROR)


# TODO 1: LLM setup
# Initialize your client here, same as in agent.py.

client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
MODEL_FALLBACKS = [
    "gemini-3.5-flash-lite",   
    "gemini-3.5-flash",
    "gemini-3.6-flash",
    "gemini-3.7-flash",
    "gemini-3.8-flash",
    "gemini-flash-lite-latest",
    "gemini-flash-latest",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
]

def _call_llm_with_retry(prompt: str, max_retries_per_model: int = 2) -> str:

    last_error = None

    for model_name in MODEL_FALLBACKS:
        for attempt in range(max_retries_per_model):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                )
                return response.text.strip()
            except Exception as e:
                last_error = e
                wait_time = 2 ** attempt
                time.sleep(wait_time)
      

    raise RuntimeError(f"Ningún modelo respondió. Último error: {last_error}")



# TODO 2: Implement the evaluator
def evaluate(query: str, tool_outputs: dict, agent_answer: str) -> dict:
    """
    Call an LLM to evaluate the agent's response.
    """
    judge_prompt = f"""You are an independent quality judge for an AI agent's
response. You did NOT generate this response — you are auditing it.

Original user query:
{query}

Raw tool outputs available to the agent (its ONLY valid source of truth):
{json.dumps(tool_outputs, indent=2, default=str)}

Agent's final answer:
{agent_answer}

Evaluate on exactly three criteria:
1. GROUNDING: Does every factual claim in the agent's answer trace back to
   the tool outputs above? Flag any invented data.
2. CITATIONS: Did the agent correctly cite 'Role-DB' for role data and the
   correct 'source_id' for document data?
3. RELEVANCE: Does the answer directly and appropriately address the user's
   query, GIVEN the system's actual scope? A polite, correct refusal to an
   out-of-scope query (e.g. asking to order food) IS a relevant and correct
   response — the agent is not expected to fulfill requests outside its
   domain, only to handle them appropriately.

If the tool outputs are empty (e.g. an out-of-scope query with a polite
refusal), grounding and citations should both be considered PASS by default,
since no factual claims were made. Relevance should also PASS if the refusal
is appropriate and matches the query's out-of-scope nature.

Respond with ONLY a valid JSON object (no markdown, no extra text) in this
exact shape:
{{
  "grounding_ok": true or false,
  "citation_ok": true or false,
  "relevance_ok": true or false,
  "score": "PASS" or "FAIL",
  "reasoning": "one or two sentence explanation"
}}
"""

    raw_text = _call_llm_with_retry(judge_prompt)
    raw_text = raw_text.replace("```json", "").replace("```", "").strip()

    try:
        result = json.loads(raw_text)
    except json.JSONDecodeError:
        result = {
            "grounding_ok": False,
            "citation_ok": False,
            "relevance_ok": False,
            "score": "FAIL",
            "reasoning": f"Evaluator returned non-JSON output: {raw_text[:200]}",
        }

    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python evaluator.py "<query>"')
        sys.exit(1)

    query = " ".join(sys.argv[1:])

    from agent import run_agent
    agent_answer, tool_outputs = run_agent(query)

    verdict = evaluate(query, tool_outputs, agent_answer)

    print(f"\n{'═' * 60}")
    print(f"  EXTERNAL EVALUATOR")
    print(f"{'═' * 60}")
    print(f"  Query: {query!r}")
    print(f"  Agent answer: {agent_answer}")
    print(f"\n  Grounding OK : {verdict['grounding_ok']}")
    print(f"  Citation  OK : {verdict['citation_ok']}")
    print(f"  Relevance OK : {verdict['relevance_ok']}")
    print(f"  Score        : {verdict['score']}")
    print(f"  Reasoning    : {verdict['reasoning']}")
    print(f"{'═' * 60}\n")