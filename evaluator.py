"""
evaluator.py — External Evaluator skeleton (Bonus).

This component is INDEPENDENT of the agent loop.
It acts as an external judge that critiques the agent's output.

It receives:
  1. The original user query
  2. The raw tool outputs
  3. The agent's final answer and citations

And it returns a score with reasoning on three criteria:
  - GROUNDING  : Did the agent avoid hallucinating data not in the tool output?
  - CITATIONS  : Did the agent correctly map findings to source_ids?
  - RELEVANCE  : Did the agent directly answer the user's question?

Usage:
    python evaluator.py "What role does Priya own?"
"""

import sys

# TODO: import your preferred LLM SDK
# import openai
# import anthropic


# ===========================================================================
# EVALUATOR FUNCTION
# ===========================================================================
# TODO: Implement an LLM call that judges the agent's output.
#
# The evaluator must be completely separate from the agent —
# it should not import or call any agent functions directly.
# It only receives the three inputs listed above.
#
# Suggested LLM prompt structure:
#   System: "You are an impartial judge evaluating an access review agent..."
#   User:   JSON blob of { query, tool_output, agent_answer, sources }
#
# The LLM should return a structured verdict, for example:
#   {
#     "grounding_ok": true,
#     "citation_ok":  true,
#     "relevance_ok": true,
#     "score":        "PASS",
#     "reasoning":    "All claims trace to tool output. Citations are valid."
#   }

def evaluate(
    query:        str,
    tool_outputs: dict,
    agent_answer: str,
    sources:      list[str],
) -> dict:
    """
    Call an LLM to evaluate the agent's response.

    Args:
        query:        The original user question.
        tool_outputs: Raw output from role_tool and document_tool.
        agent_answer: The agent's final natural-language response.
        sources:      The source_ids the agent cited.

    Returns:
        A dict with keys: grounding_ok, citation_ok, relevance_ok, score, reasoning.
    """
    # TODO
    raise NotImplementedError


# ===========================================================================
# CLI — run the agent and then evaluate its output
# ===========================================================================

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python evaluator.py \"<query>\"")
        sys.exit(1)

    query = " ".join(sys.argv[1:])

    # TODO: Run the agent's routing + tool calls to capture its inputs/outputs,
    #       then call evaluate() and print the verdict.
    #
    # Hint: you can import route() and execute_tools() from agent.py,
    #       or re-run the agent as a subprocess and parse its output.

    print("Evaluator not yet implemented.")