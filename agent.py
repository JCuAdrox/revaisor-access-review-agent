"""
agent.py — RevAIsor Access Review Agent

Run from the command line:
    python agent.py "What role does Priya own?"
    python agent.py "What is the difference between GBR and ZGBR?"
    python agent.py "Show me Priya's access review history."
    python agent.py "Order a pizza for the office"

Your tasks:
  1. Set your API key in the environment.
  2. Implement build_system_prompt()
  3. Implement run_agent()
  4. Implement verify_response()
"""

from __future__ import annotations

import sys
import json
import os
import re

# LLM SDKs — choose one
import openai
from google import genai

from tools import role_tool, document_tool
from router import route

# TODO 1: LLM setup
# TODO: initialize your client


# Tool registry — maps tool names to functions
TOOLS = {
    "role_tool":     role_tool,
    "document_tool": document_tool,
}


# TODO 2: Build the system prompt
def build_system_prompt() -> str:
    """
    Build the system prompt that defines the agent's behavior.

    Must include:
      - The agent's role and scope (access review only)
      - Citation rules: cite 'Role-DB' for role_tool, cite source_id for document_tool
      - Out-of-scope instructions: refuse politely without calling any tools
    """
    raise NotImplementedError

# TODO 3: Agent loop
def run_agent(query: str) -> str:
    """
    Main agent loop.

    Flow:
      1. Call route(query) to get intent, entities, and tools_to_call
      2. If out_of_scope, return a polite refusal without calling the LLM
      3. Execute the tools specified in tools_to_call
      4. Send system prompt + query + tool results to the LLM
      5. Return the final cited response

    Args:
        query: The raw user query string.

    Returns:
        str — the agent's final cited response.
    """
    raise NotImplementedError

# TODO 4: Verifier
def verify_response(query: str, response: str) -> dict:
    """
    Rule-based check on the agent's final response. No LLM call.

    Checks:
      1. citation_present  : does the response mention at least one valid source_id?
      2. no_invented_roles : does the response mention role IDs not in the KG?

    Returns:
        {
            "status": "SUCCESS" | "FAIL",
            "checks": [
                { "name": str, "passed": bool, "detail": str },
                ...
            ]
        }
    """
    raise NotImplementedError

# Entry point
def _print_section(title: str, content: str) -> None:
    width = 60
    print(f"\n{'─' * width}")
    print(f"  {title}")
    print(f"{'─' * width}")
    print(content)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python agent.py "<your query>"')
        sys.exit(1)

    user_query = sys.argv[1]

    print(f"\n{'═' * 60}")
    print(f"  REVAISOR ACCESS REVIEW AGENT")
    print(f"{'═' * 60}")
    print(f"  Query: {user_query!r}")

    response = run_agent(user_query)
    _print_section("AGENT ANSWER", response)

    verification = verify_response(user_query, response)
    status = verification["status"]
    checks = "\n".join(
        f"  {'✓' if c['passed'] else '✗'} {c['name']}: {c['detail']}"
        for c in verification["checks"]
    )
    _print_section("VERIFICATION", f"Status: {status}\n{checks}")

    print(f"\n{'═' * 60}\n")