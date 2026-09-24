"""
router.py — Router for the RevAIsor Access Review Agent.

Your task: implement the router that analyzes the user query and decides
which tools to call before passing control to the agent loop.

The router runs before any LLM or tool call — it should be fast and
deterministic, based on the Knowledge Graph and simple keyword matching.
"""

from knowledge_graph import KG


# TODO 1: Entity extraction
def extract_entities(query: str) -> dict:
    """
    Parse the query and identify known entities.
    """
    query_lower = query.lower()

    users_found = [
        name for name in KG["users"]
        if name.lower() in query_lower
    ]

    role_types_found = [
        role for role in KG["role_types"]
        if role.lower() in query_lower
    ]

    return{
        "users": users_found,
        "role_types": role_types_found,
    }

# TODO 2: Intent classification
def classify_intent(query: str, entities: dict) -> str:
    """
    Determine the intent of the query.
    """
    query_lower = query.lower()

    comparison_keywords = ["difference", "compare", "comparison", "vs", "versus"]
    history_keywords = ["history", "review history", "past reviews", "audit"]
    ownership_keywords = ["role", "own", "owns", "ownership", "which role", "what role"]

    has_user = len(entities["users"]) > 0
    has_role_type = len(entities["role_types"]) > 0

    # Comparison: explicit comparison keywords, or two types mentioned together
    if any(kw in query_lower for kw in comparison_keywords) and (has_role_type or len(entities["role.types"]) >=1):
        return "role_comparison"

    # Access history: explicit history keywords + a know user
    if any(kw in query_lower for kw in history_keywords) and has_user:
        return "access_history"

    # Role ownership: a know user + ownership-related keyword
    if has_user and any(kw in query_lower for kw in ownership_keywords):
        return "role_ownership"

    #fallback: if we found entities but no clear intent, default to
    # roles_ownership if there's a user, or role_comparison if there's a role_type
    if has_user:
        return "role_ownership"
    if has_role_type:
        return "role_comparison"

    #nothing recognized at all: out of scope
    return "out_of_scope"

# TODO 3: Tool selection
def select_tools(intent: str) -> list:
    """
    Given the intent, return the list of tool names to call.
    """
    mapping = {
        "role_ownership": ["role_tool"],
        "access_history": ["role_tool"],
        "role_comparison": ["document_tool"],
        "out_of_scope": [],
    }
    return mapping.get(intent, [])

# TODO 4: Main router entry point
def route(query: str) -> dict:
    """
    Main entry point. Given a raw query, return a routing decision.
    """
    entities = extract_entities(query)
    intent = classify_intent(query, entities)
    tools_to_call = select_tools(intent)

    return {
        "intent": intent,
        "entities": entities,
        "tools_to_call": tools_to_call
    }