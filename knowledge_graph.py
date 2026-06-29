"""
knowledge_graph.py
"""

KG: dict = {
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
    ],
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
    },

}