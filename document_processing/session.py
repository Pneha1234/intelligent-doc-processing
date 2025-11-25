"""
Session and memory management utilities.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class InMemorySessionService:
    """
    Simple in-memory session management for maintaining state across agents.
    """

    def __init__(self):
        self.sessions: Dict[str, Dict[str, Any]] = {}
        logger.info("Session service initialized")

    def create_session(self, session_id: str) -> Dict[str, Any]:
        """Create new session."""
        self.sessions[session_id] = {
            "id": session_id,
            "created_at": datetime.now().isoformat(),
            "state": {},
            "history": [],
        }
        logger.info("Created session: %s", session_id)
        return self.sessions[session_id]

    def get_session(self, session_id: str) -> Dict[str, Any] | None:
        """Retrieve session."""
        return self.sessions.get(session_id)

    def update_state(self, session_id: str, key: str, value: Any):
        """Update session state."""
        if session_id not in self.sessions:
            return

        self.sessions[session_id]["state"][key] = value
        self.sessions[session_id]["history"].append(
            {
                "timestamp": datetime.now().isoformat(),
                "action": f"Updated {key}",
                "value": str(value)[:100],  # Truncate for logging
            }
        )
        logger.debug("Session %s: Updated %s", session_id, key)

    def get_state(self, session_id: str, key: str) -> Any:
        """Get state value."""
        session = self.get_session(session_id)
        return session["state"].get(key) if session else None


class MemoryBank:
    """
    Long-term memory for storing document processing patterns.
    """

    def __init__(self):
        self.patterns: Dict[str, List[Dict[str, Any]]] = {
            "invoice_patterns": [],
            "contract_patterns": [],
            "common_entities": [],
            "action_templates": [],
        }
        logger.info("Memory bank initialized")

    def store_pattern(self, doc_type: str, pattern: Dict[str, Any]):
        """Store learned pattern."""
        key = f"{doc_type.lower()}_patterns"
        if key in self.patterns:
            self.patterns[key].append(pattern)
            logger.debug("Stored pattern for %s", doc_type)

    def retrieve_patterns(self, doc_type: str) -> List[Dict[str, Any]]:
        """Retrieve patterns for document type."""
        key = f"{doc_type.lower()}_patterns"
        return self.patterns.get(key, [])

