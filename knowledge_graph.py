"""
knowledge_graph.py 

Your task: fill in the KG with the data your tools will query.

The KG must encode:
  1. Role types      : GBR and ZGBR with their defining attributes
  2. Policy documents: fragments your document_tool will search over
  3. Users           : who owns which roles, and their review history

Your tools.py will import KG and query it directly.

You are free to restructure KG as long as your tools can query it correctly.
"""

KG: dict = {

    # ── Role Types ────────────────────────────────────────────────────────
    # TODO: complete the GBR entry and add ZGBR.
    # Each role type should have enough data for the agent to answer:
    #   - "What is a GBR / ZGBR?"
    #   - "What is the difference between GBR and ZGBR?"
    "role_types": {
        "GBR": {
            "full_name": "Global Business Role",
            "access_model": "persistent",
            "session_verification": False,
            "description": (
                "Grants broad, persistent access across the organization. "
                "Access is validated at assignment time and does not require "
                "per-session re-verification."
            ),
            "differs_from": "ZGBR",
        },
    },

    # ── Policy Documents ──────────────────────────────────────────────────
    # TODO: add more documents.
    # Each document must have a source_id — the agent must cite it in responses.
    "documents": [
        {
            "source_id": "Policy-Doc-GBR-001",
            "title":     "GBR Access Policy",
            "content":   (
                "A Global Business Role (GBR) grants broad, persistent access "
                "to resources across the organization. Access is validated at "
                "the time of role assignment and does not require per-session "
                "verification."
            ),
            "keywords":  ["GBR", "global business role", "broad", "persistent"],
        },
        # TODO: add Policy-Doc-ZGBR-002 and Policy-Doc-CMP-003
    ],

    # ── Users ─────────────────────────────────────────────────────────────
    # TODO: add more users. 
    # Each user should have enough data for the agent to answer:
    #   - "What role does <user> own?"
    #   - "Show me <user>'s access review history."
    "users": {
        "Priya": {
            "owns":       ["GBR-1234"],
            "role_type":  "GBR",
            "department": "Engineering",
            "review_history": [
                {"date": "2024-01-15", "status": "APPROVED", "reviewer": "Alice"},
                {"date": "2024-07-10", "status": "APPROVED", "reviewer": "Bob"},
                {"date": "2025-01-20", "status": "PENDING",  "reviewer": None},
            ],
        },
        # TODO: add other users 
    },

}