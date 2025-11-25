"""
Main orchestrator coordinating the sequential agent pipeline.
"""

from __future__ import annotations

import logging
from dataclasses import asdict
from datetime import datetime

from .agents import (
    ActionItemsAgent,
    DocumentClassifierAgent,
    InformationExtractionAgent,
    RiskAssessmentAgent,
    SummaryGenerationAgent,
)
from .models import ProcessingResult
from .session import InMemorySessionService, MemoryBank

logger = logging.getLogger(__name__)


class DocumentProcessingOrchestrator:
    """Coordinates all agents in sequence."""

    def __init__(self):
        self.session_service = InMemorySessionService()
        self.memory_bank = MemoryBank()

        self.classifier = DocumentClassifierAgent(self.memory_bank)
        self.extractor = InformationExtractionAgent(self.session_service)
        self.action_agent = ActionItemsAgent()
        self.summarizer = SummaryGenerationAgent()
        self.risk_assessor = RiskAssessmentAgent()

        logger.info("DocumentProcessingOrchestrator initialized")

    def process_document(self, document_text: str, document_id: str | None = None) -> ProcessingResult:
        """Main processing pipeline."""
        start_time = datetime.now()

        if not document_id:
            document_id = f"doc_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        logger.info("=== Starting document processing: %s ===", document_id)

        session_id = f"session_{document_id}"
        self.session_service.create_session(session_id)

        doc_type, confidence = self.classifier.classify(document_text)
        self.session_service.update_state(session_id, "doc_type", doc_type)
        self.session_service.update_state(session_id, "confidence", confidence)

        metadata = self.extractor.extract(document_text, session_id)
        self.session_service.update_state(session_id, "metadata", asdict(metadata))

        action_items = self.action_agent.identify_actions(metadata, document_text)
        self.session_service.update_state(
            session_id, "action_items", [asdict(a) for a in action_items]
        )

        summary = self.summarizer.generate_summary(metadata, action_items)
        self.session_service.update_state(session_id, "summary", summary)

        risks = self.risk_assessor.assess_risks(metadata, document_text)
        self.session_service.update_state(session_id, "risks", [asdict(r) for r in risks])

        processing_time = (datetime.now() - start_time).total_seconds() * 1000

        self.memory_bank.store_pattern(
            doc_type,
            {
                "entities_found": len(metadata.dates) + len(metadata.amounts),
                "action_count": len(action_items),
                "risk_level": max(
                    [r.level for r in risks],
                    key=lambda x: {"High": 3, "Medium": 2, "Low": 1}[x],
                ),
            },
        )

        result = ProcessingResult(
            document_id=document_id,
            timestamp=datetime.now().isoformat(),
            metadata=metadata,
            action_items=action_items,
            summary=summary,
            risks=risks,
            processing_time_ms=int(processing_time),
        )

        logger.info("=== Processing complete: %s (%.2fms) ===", document_id, processing_time)
        return result

