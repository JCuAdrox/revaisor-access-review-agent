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

# LLM SDKs — choose one
import openai
from google import genai

# ---------------------------------------------------------------------------
# TODO 1: LLM setup
# ---------------------------------------------------------------------------
# Initialize your client here, same as in agent.py.

# ---------------------------------------------------------------------------
# TODO 2: Implement the evaluator
# ---------------------------------------------------------------------------

def evaluate(
    query:        str,
    tool_outputs: dict,
    agent_answer: str,
) -> dict:
    """
    Call an LLM to evaluate the agent's response.

    Args:
        query:        The original user question.
        tool_outputs: Raw output from all tool calls made by the agent.
        agent_answer: The agent's final natural-language response.

    Returns:
        A dict with keys: grounding_ok, citation_ok, relevance_ok, score, reasoning.
        Example:
        {
            "grounding_ok": True,
            "citation_ok":  True,
            "relevance_ok": True,
            "score":        "PASS",
            "reasoning":    "All claims trace to tool output. Citations are valid."
        }
    """
    # TODO: implement this
    raise NotImplementedError


# ---------------------------------------------------------------------------
# TODO 3: Run the agent and evaluate its output
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python evaluator.py "<query>"')
        sys.exit(1)

    query = " ".join(sys.argv[1:])

    # TODO: 
    #   1. Import and run the agent to get the answer and capture tool outputs
    #   2. Call evaluate() with the results
    #   3. Print the verdict
    #
    # Hint: you can wrap the functions in agent.TOOLS to intercept
    #       and record what each tool returned during the agent run.

    print("Evaluator not yet implemented.")