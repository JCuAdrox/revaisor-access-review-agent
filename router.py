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

    Returns:
        {
            "users":      list[str],  — names found in query that exist in KG
            "role_types": list[str],  — role type names found (e.g. ["GBR", "ZGBR"])
        }

    TODO: scan KG["users"] and KG["role_types"] for matches in the query.
          Use case-insensitive matching.

    Example:
        >>> extract_entities("What role does Priya own?")
        {"users": ["Priya"], "role_types": []}

        >>> extract_entities("Compare GBR and ZGBR")
        {"users": [], "role_types": ["GBR", "ZGBR"]}
    """
    raise NotImplementedError

# TODO 2: Intent classification
def classify_intent(query: str, entities: dict) -> str:
    """
    Determine the intent of the query.

    Returns one of:
        "role_ownership"  — user wants to know what role someone owns
        "role_comparison" — user wants to compare two role types
        "access_history"  — user wants to see a user's review history
        "out_of_scope"    — query has nothing to do with access review

    TODO: use keyword matching on the query and the extracted entities.

    Example:
        >>> classify_intent("What role does Priya own?", {"users": ["Priya"], ...})
        "role_ownership"

        >>> classify_intent("Order a pizza", {})
        "out_of_scope"
    """
    raise NotImplementedError

# TODO 3: Tool selection
def select_tools(intent: str) -> list:
    """
    Given the intent, return the list of tool names to call.

    Returns a list of tool names: "role_tool", "document_tool", or both.
    Returns an empty list for out_of_scope.

    Suggested mapping:
        role_ownership  → ["role_tool"]
        access_history  → ["role_tool"]
        role_comparison → ["document_tool"]
        out_of_scope    → []
    """
    raise NotImplementedError


# TODO 4: Main router entry point
def route(query: str) -> dict:
    """
    Main entry point. Given a raw query, return a routing decision.

    Returns:
        {
            "intent":        str,
            "entities":      dict,
            "tools_to_call": list[str],
        }

    TODO: orchestrate extract_entities → classify_intent → select_tools.
    """
    raise NotImplementedError