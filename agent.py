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
import time
import logging

# LLM SDKs — choose one
import openai
from google import genai

from tools import role_tool, document_tool
from router import route
from knowledge_graph import KG

logging.getLogger("google_genai").setLevel(logging.ERROR)
logging.getLogger("google_genai.models").setLevel(logging.ERROR)


# TODO 1: LLM setup
client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
MODEL_NAME = "gemini-2.5-flash"  

MODEL_FALLBACKS = [
    "gemini-3.5-flash-lite",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.5-pro",
    "gemini-3.5-flash",
    "gemini-3.7-flash",
    "gemini-3.8-flash",
    "gemini-3.6-flash",
    "gemini-flash-lite-latest",
    "gemini-flash-latest",
    "gemini-pro-latest",
]

# TODO: initialize your client

# Tool registry — maps tool names to functions
TOOLS = {
    "role_tool":     role_tool,
    "document_tool": document_tool,
}


# TODO 2: Build the system prompt
def build_system_prompt() -> str:
    return """You are the RevAIsor Access Review Agent, an assistant that helps
security teams understand internal access roles and policies.

SCOPE:
- You ONLY answer questions about role ownership, role types (GBR, ZGBR),
  access policy comparisons, and access review history.
- You do NOT answer questions unrelated to access review (e.g. ordering food,
  scheduling, general chit-chat). If asked something out of scope, politely
  decline and state that you only handle access review queries.

CITATION RULES (MANDATORY):
- When your answer uses data returned by role_tool, cite it as (Source: Role-DB).
- When your answer uses data returned by document_tool, cite the exact
  'source_id' field from that document, e.g. (Source: Policy-Doc-GBR-001).
- Every factual claim in your response must be traceable to a citation.
- NEVER state a role ID, department, or policy detail that does not appear
  in the tool output provided to you. Do not invent or assume data.

STYLE:
- Be concise, clear, and professional.
- If the tool output contains an error (e.g. user not found), state that
  clearly instead of guessing.
"""

def _call_llm_with_retry(system_prompt: str, user_message: str, max_retries_per_model: int = 2):
    """
        Try generating content by testing various models in order, with retries per model, until one responds or the list is exhausted.
    """
    last_error = None

    for model_name in MODEL_FALLBACKS:
        for attempt in range(max_retries_per_model):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=user_message,
                    config={"system_instruction": system_prompt},
                )
                return response.text.strip()
            except Exception as e:
                last_error = e
                wait_time = 2 ** attempt
                time.sleep(wait_time)

    raise RuntimeError(
        f"No model in the list responded. Last error: {last_error}"
    )



# TODO 3: Agent loop
def run_agent(query: str) -> tuple[str, dict]:
    """
    Main agent loop.
    """
    routing = route(query)

    if routing["intent"] == "out_of_scope":
        return (
            "I'm sorry, but that request is outside the scope of the Access "
            "Review Agent. I can only help with questions about role "
            "ownership, role type comparisons (GBR/ZGBR), and access review "
            "history.",
            {},
        )

    tool_outputs = {}
    for tool_name in routing["tools_to_call"]:
        tool_fn = TOOLS[tool_name]
        if tool_name == "role_tool":
            for user in routing["entities"]["users"]:
                tool_outputs.setdefault("role_tool", {})[user] = tool_fn(user)
        elif tool_name == "document_tool":
            tool_outputs["document_tool"] = tool_fn(query)

    system_prompt = build_system_prompt()
    user_message = f"""User query: {query}

Detected entities: {json.dumps(routing["entities"])}
Detected intent: {routing["intent"]}

Tool outputs (this is your ONLY source of truth — do not use outside knowledge):
{json.dumps(tool_outputs, indent=2, default=str)}

Compose the final answer following the citation rules exactly."""

    response_text = _call_llm_with_retry(system_prompt, user_message)

    return response_text, tool_outputs


# TODO 4: Verifier
def verify_response(query: str, response: str) -> dict:
    """
    Rule-based check on the agent's final response. No LLM call.
    """
    checks = []

    all_valid_source_ids = [doc["source_id"] for doc in KG["documents"]]

    # out of scope
    is_out_of_scope = "outside the scope of the Access Review Agent" in response

    # citation_present 
    if is_out_of_scope:
        checks.append({
            "name": "citation_present",
            "passed": True,
            "detail": "Out-of-scope response — no citation required.",
        })
    else:
        found_citations = [
            sid for sid in all_valid_source_ids + ["Role-DB"] if sid in response
        ]
        citation_present = len(found_citations) > 0
        checks.append({
            "name": "citation_present",
            "passed": citation_present,
            "detail": (
                f"Found citation(s): {found_citations}" if citation_present
                else "No valid source_id or 'Role-DB' citation found in response."
            ),
        })

    # no_invented_roles 
    # We remove source_ids from the text BEFORE searching for role IDs,
    # to avoid confusing citation fragments (e.g., "GBR-001" within
    # "Policy-Doc-GBR-001") with actual invented role IDs.
    text_without_citations = response
    for sid in all_valid_source_ids:
        text_without_citations = text_without_citations.replace(sid, "")

    all_known_role_ids = []
    for user_data in KG["users"].values():
        all_known_role_ids.extend(user_data["owns"])

    mentioned_role_ids = re.findall(r"\b[A-Z]{3,4}-\d{3,4}\b", text_without_citations)
    invented = [rid for rid in mentioned_role_ids if rid not in all_known_role_ids]
    no_invented_roles = len(invented) == 0

    checks.append({
        "name": "no_invented_roles",
        "passed": no_invented_roles,
        "detail": (
            "No invented role IDs detected." if no_invented_roles
            else f"Found role ID(s) not present in the Knowledge Graph: {invented}"
        ),
    })

    status = "SUCCESS" if all(c["passed"] for c in checks) else "FAIL"

    return {"status": status, "checks": checks}


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

    response, tool_outputs = run_agent(user_query)  
    _print_section("AGENT ANSWER", response)

    verification = verify_response(user_query, response)
    status = verification["status"]
    checks = "\n".join(
        f"  {'✓' if c['passed'] else '✗'} {c['name']}: {c['detail']}"
        for c in verification["checks"]
    )
    _print_section("VERIFICATION", f"Status: {status}\n{checks}")

    print(f"\n{'═' * 60}\n")