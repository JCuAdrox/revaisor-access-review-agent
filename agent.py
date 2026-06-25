"""
agent.py

Run from the command line:
    python agent.py "What role does Priya own?"
    python agent.py "What is the difference between GBR and ZGBR?"
    python agent.py "Show me Priya's access review history."
    python agent.py "Order a pizza for the office"

Your tasks:
  1. Set your API key (OpenAI or Gemini) in the environment or below.
  2. Define TOOLS and TOOL_SCHEMAS
  3. Implement build_system_prompt()
  4. Implement run_agent()
  5. Implement verify_response()
"""

from __future__ import annotations

import sys
import json

# LLM SDKs — choose one
import openai
from google import genai

from tools import role_tool, document_tool, get_user, get_role_type, get_contrast

# ---------------------------------------------------------------------------
# TODO 1: LLM setup
# ---------------------------------------------------------------------------
# Initialize your client here. Load keys from environment variables.
#
# TODO: initialize your client


# ---------------------------------------------------------------------------
# TODO 2: Tool registry and schemas
# ---------------------------------------------------------------------------
# Define TOOLS — a dict mapping tool name → function.
# Define TOOL_SCHEMAS — a list describing each tool to the LLM.
#
# TODO: define TOOLS and TOOL_SCHEMAS
TOOLS = {}
TOOL_SCHEMAS = []


# ---------------------------------------------------------------------------
# TODO 3: Build the system prompt
# ---------------------------------------------------------------------------

def build_system_prompt() -> str:
    """
    Build the system prompt that defines the agent's behavior.

    Must include:
      - The agent's role and scope (access review only)
      - Citation rules: cite 'Role-DB' for role_tool, cite source_id for document_tool
      - Out-of-scope instructions: if the query is unrelated to access review,
        refuse politely without calling any tools

    Returns:
        str — the complete system prompt
    """
    # TODO: implement this
    raise NotImplementedError


# ---------------------------------------------------------------------------
# TODO 4: Agent loop
# ---------------------------------------------------------------------------

def run_agent(query: str) -> str:
    """
    Main agent loop. Sends the query to the LLM, handles tool calls,
    and returns the final natural-language response.

    Flow:
      1. Send system prompt + user query to the LLM
      2. If the LLM requests a tool call:
           a. Execute the tool from TOOLS
           b. Send the result back to the LLM
           c. Repeat until the LLM returns a final text response
      3. Return the final response

    Args:
        query: The raw user query string.

    Returns:
        str — the agent's final cited response.

    Hints:
      - Use a loop to handle multiple tool calls in sequence.
      - The LLM decides which tools to call and in what order.
    """
    # TODO: implement this
    raise NotImplementedError


# ---------------------------------------------------------------------------
# TODO 5: Verifier
# ---------------------------------------------------------------------------

def verify_response(query: str, response: str) -> dict:
    """
    Rule-based check on the agent's final response.
    
    Checks:
      1. citation_present  : does the response mention at least one source_id?
                             Valid source IDs: "Role-DB", "Policy-Doc-GBR-001",
                             "Policy-Doc-ZGBR-002", "Policy-Doc-CMP-003"
      2. no_invented_roles : does the response mention any role IDs (e.g. GBR-XXXX)
                             that are NOT in the KG?

    Args:
        query    : the original user query
        response : the agent's final response string

    Returns:
        dict:
        {
            "status": "SUCCESS" | "WARNING" | "FAIL",
            "checks": [
                { "name": str, "passed": bool, "detail": str },
                ...
            ]
        }
    """
    # TODO: implement this
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def _print_section(title: str, content: str) -> None:
    width = 60
    print(f"\n{'─' * width}")
    print(f"  {title}")
    print(f"{'─' * width}")
    print(content)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python agent.py "<your query>"')
        print('Example: python agent.py "What role does Priya own?"')
        sys.exit(1)

    user_query = sys.argv[1]

    print(f"\n{'═' * 60}")
    print(f"  REVAISOR ACCESS REVIEW AGENT")
    print(f"{'═' * 60}")
    print(f"  Query: {user_query!r}")

    # Run agent
    response = run_agent(user_query)
    _print_section("AGENT ANSWER", response)

    # Verify
    verification = verify_response(user_query, response)
    status = verification["status"]
    checks = "\n".join(
        f"  {'✓' if c['passed'] else '✗'} {c['name']}: {c['detail']}"
        for c in verification["checks"]
    )
    _print_section("VERIFICATION", f"Status: {status}\n{checks}")

    print(f"\n{'═' * 60}\n")