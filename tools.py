"""
tools.py

Each function is a tool the agent can call. They all query the Knowledge Graph
defined in knowledge_graph.py — there is no other data source.

Your tasks:
  1. Fill in the KG data in knowledge_graph.py
  2. Implement each function below so it queries KG correctly
  
Citation rule: every tool that returns data must make it easy for the agent
to cite its source. role_tool cites "Role-DB", document_tool cites the
source_id field in each document fragment.
"""

from knowledge_graph import KG


# ---------------------------------------------------------------------------
# User & role tools
# ---------------------------------------------------------------------------

def role_tool(user_id: str) -> dict:
    """
    Retrieve ownership and review history for a given user.

    Args:
        user_id: The user's display name, e.g. "Priya".

    Returns:
        {
            "<user_id>": {
                "owns":           list[str],
                "role_type":      str,
                "department":     str,
                "review_history": list[dict]
            }
        }
        or {"error": "..."} if the user is not found.

    Source: always cite as "Role-DB" in the agent response.

    TODO: query KG["users"] and return the matching user data.
          Handle case-insensitive lookup and missing users gracefully.
    """
    raise NotImplementedError

# ---------------------------------------------------------------------------
# Document tool
# ---------------------------------------------------------------------------

def document_tool(query: str) -> list[dict]:
    """
    Return policy document fragments matching the query.

    Args:
        query: A natural-language or keyword search string,
               e.g. "difference between GBR and ZGBR".

    Returns:
        A list of matching document dicts, each containing:
        {
            "source_id": str,   ← the agent MUST cite this
            "title":     str,
            "content":   str,
            "keywords":  list[str]
        }
        Returns an empty list if no documents match.

    TODO: search KG["documents"] and return fragments whose keywords
          overlap with the query. Use case-insensitive matching.
    """
    raise NotImplementedError