"""
ADK integration that exposes the orchestrator via an Agent Development Kit agent.
"""

from __future__ import annotations

from typing import Any, Dict

from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import FunctionTool

from .config import settings
from .orchestrator import DocumentProcessingOrchestrator


class DocumentProcessingADKApp:
    """
    Thin wrapper that binds the orchestrator to an ADK agent so it can be used
    from the ADK web UI or runners.
    """

    def __init__(self):
        self.orchestrator = DocumentProcessingOrchestrator()
        self.model = Gemini(model=settings.google_model)

        self.process_document_tool = FunctionTool(self._process_document_tool)

        self.agent = Agent(
            name="DocumentProcessingAgent",
            instruction=(
                "You are an enterprise document processing assistant. "
                "Use the provided tool to run the deterministic multi-agent pipeline "
                "and report the structured results back to the user."
            ),
            model=self.model,
            tools=[self.process_document_tool],
        )
        self.runner = InMemoryRunner(self.agent)

    def _process_document_tool(
        self,
        document_text: str,
        document_id: str | None = None,
    ) -> Dict[str, Any]:
        """
        Execute the orchestrator pipeline on the provided document text and
        return structured JSON for the ADK agent.
        """
        result = self.orchestrator.process_document(document_text, document_id)
        payload: Dict[str, Any] = {
            "document_id": result.document_id,
            "doc_type": result.metadata.doc_type,
            "confidence": result.metadata.confidence,
            "dates": result.metadata.dates,
            "amounts": result.metadata.amounts,
            "parties": result.metadata.parties,
            "references": result.metadata.references,
            "summary": result.summary,
            "action_items": [vars(a) for a in result.action_items],
            "risks": [vars(r) for r in result.risks],
            "processing_time_ms": result.processing_time_ms,
        }

        return payload

    def run_conversation(self, message: str) -> Any:
        """Utility for CLI/testing without the ADK web UI."""
        return self.runner.run(message)

