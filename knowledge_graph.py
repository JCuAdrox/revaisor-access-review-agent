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
        "ZGBR": {
            "full_name": "Zero-Trust Global Business Role",
            "access_model": "per-session",
            "session_verification": True,
            "description": (
                "Enforces per-session verification via MFA or just-in-time "
                "(JIT) approval. Used for privileged access to sensitive systems."
            ),
            "differs_from": "GBR",
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
        {
            "source_id": "Policy-Doc-ZGBR-002",
            "title":     "ZGBR Access Policy",
            "content":   (
                "A Zero-Trust Global Business Role (ZGBR) enforces per-session "
                "verification via MFA or just-in-time (JIT) approval. Used for "
                "privileged access to sensitive systems."
            ),
            "keywords":  ["ZGBR", "zero trust", "per-session", "JIT", "MFA"],
        },
        {
            "source_id": "Policy-Doc-CMP-003",
            "title":     "GBR vs ZGBR Comparison",
            "content":   (
                "The key distinction between a GBR and a ZGBR is access persistence. "
                "A GBR provides standing access that does not require re-validation "
                "per session. A ZGBR enforces real-time, per-session verification "
                "aligned with zero-trust principles. ZGBR is typically assigned to "
                "roles with elevated data sensitivity."
            ),
            "keywords":  ["difference", "compare", "comparison", "GBR", "ZGBR", "vs"],
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
        "Carlos": {
            "owns":       ["ZGBR-5678"],
            "role_type":  "ZGBR",
            "department": "Finance",
            "review_history": [
                {"date": "2024-03-10", "status": "APPROVED", "reviewer": "Carol"},
                {"date": "2024-09-18", "status": "FLAGGED",  "reviewer": "Carol"},
                {"date": "2025-02-05", "status": "APPROVED", "reviewer": "Dave"},
            ],
        },
        "Fatima": {
            "owns":       ["GBR-9999", "ZGBR-0001"],
            "role_type":  "mixed",
            "department": "Security",
            "review_history": [
                {"date": "2024-02-20", "status": "APPROVED", "reviewer": "Eve"},
                {"date": "2024-08-14", "status": "APPROVED", "reviewer": "Alice"},
                {"date": "2025-03-01", "status": "PENDING",  "reviewer": None},
            ],
        },
    },
}