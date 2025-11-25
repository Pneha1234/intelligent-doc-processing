"""
Agent implementations for each stage of the document processing pipeline.
"""

from __future__ import annotations

import logging
from typing import List

from .models import ActionItem, DocumentMetadata, RiskAssessment
from .session import InMemorySessionService, MemoryBank
from .tools import DocumentParserTool, EntityExtractionTool

logger = logging.getLogger(__name__)


class DocumentClassifierAgent:
    """Agent 1: Classifies document type."""

    def __init__(self, memory_bank: MemoryBank):
        self.memory_bank = memory_bank
        self.name = "DocumentClassifierAgent"
        logger.info("%s initialized", self.name)

    def classify(self, document_text: str) -> tuple[str, float]:
        """Classify document and return type with confidence."""
        logger.info("%s: Starting classification", self.name)

        text_lower = document_text.lower()

        if any(word in text_lower for word in ["invoice", "bill", "payment due"]):
            doc_type = "Invoice"
            confidence = 0.95
        elif any(word in text_lower for word in ["contract", "agreement", "terms and conditions"]):
            doc_type = "Contract"
            confidence = 0.90
        elif any(word in text_lower for word in ["report", "analysis", "findings", "summary"]):
            doc_type = "Report"
            confidence = 0.85
        elif any(word in text_lower for word in ["proposal", "quotation", "estimate"]):
            doc_type = "Proposal"
            confidence = 0.88
        else:
            doc_type = "General Document"
            confidence = 0.70

        logger.info("%s: Classified as %s (confidence: %.2f)", self.name, doc_type, confidence)
        return doc_type, confidence


class InformationExtractionAgent:
    """Agent 2: Extracts key information from documents."""

    def __init__(self, session_service: InMemorySessionService):
        self.session_service = session_service
        self.parser = DocumentParserTool()
        self.entity_tool = EntityExtractionTool()
        self.name = "InformationExtractionAgent"
        logger.info("%s initialized", self.name)

    def extract(self, document_text: str, session_id: str) -> DocumentMetadata:
        """Extract all key information from document."""
        logger.info("%s: Starting extraction", self.name)

        doc_type = self.session_service.get_state(session_id, "doc_type")
        confidence = self.session_service.get_state(session_id, "confidence")

        dates = self.parser.extract_dates(document_text)
        amounts = self.parser.extract_amounts(document_text)
        references = self.parser.extract_references(document_text)
        parties = self.entity_tool.extract_parties(document_text)

        metadata = DocumentMetadata(
            doc_type=doc_type or "Unknown",
            confidence=confidence or 0.0,
            dates=dates[:5],
            amounts=amounts[:5],
            parties=parties[:5],
            references=references[:5],
        )

        logger.info(
            "%s: Extracted %s dates, %s amounts, %s parties",
            self.name,
            len(dates),
            len(amounts),
            len(parties),
        )
        return metadata


class ActionItemsAgent:
    """Agent 3: Identifies required actions."""

    def __init__(self):
        self.name = "ActionItemsAgent"
        logger.info("%s initialized", self.name)

    def identify_actions(self, metadata: DocumentMetadata, document_text: str) -> List[ActionItem]:
        """Identify action items based on document type and content."""
        logger.info("%s: Identifying actions", self.name)

        actions: List[ActionItem] = []
        text_lower = document_text.lower()

        if metadata.doc_type == "Invoice":
            if metadata.dates:
                actions.append(
                    ActionItem(
                        priority="High",
                        action=f"Review and approve payment by {metadata.dates[0]}",
                        assignee="Finance Team",
                        due_date=metadata.dates[0],
                    )
                )
            actions.append(
                ActionItem(
                    priority="Medium",
                    action="Update accounting system with invoice details",
                    assignee="Accounting",
                )
            )

        elif metadata.doc_type == "Contract":
            actions.append(
                ActionItem(
                    priority="High",
                    action="Legal review required before signing",
                    assignee="Legal Team",
                )
            )
            actions.append(
                ActionItem(
                    priority="Medium",
                    action="Negotiate terms if necessary",
                    assignee="Business Development",
                )
            )

        if "urgent" in text_lower or "immediate" in text_lower:
            actions.insert(
                0,
                ActionItem(
                    priority="High",
                    action="URGENT: Immediate attention required",
                    assignee="Management",
                ),
            )

        actions.append(
            ActionItem(
                priority="Low",
                action="Archive document in appropriate folder",
                assignee="Admin",
            )
        )

        logger.info("%s: Identified %s action items", self.name, len(actions))
        return actions


class SummaryGenerationAgent:
    """Agent 4: Generates executive summary."""

    def __init__(self):
        self.name = "SummaryGenerationAgent"
        logger.info("%s initialized", self.name)

    def generate_summary(self, metadata: DocumentMetadata, action_items: List[ActionItem]) -> str:
        """Generate executive summary."""
        logger.info("%s: Generating summary", self.name)

        doc_type_desc = f"This {metadata.doc_type.lower()}"

        parties_desc = ""
        if metadata.parties:
            if len(metadata.parties) == 1:
                parties_desc = f" from {metadata.parties[0]}"
            elif len(metadata.parties) >= 2:
                parties_desc = f" involving {metadata.parties[0]} and {metadata.parties[1]}"

        financial_desc = ""
        if metadata.amounts:
            amounts_str = ", ".join(metadata.amounts[:2])
            financial_desc = f" Key financial values include {amounts_str}."

        high_priority_count = sum(1 for a in action_items if a.priority == "High")
        action_desc = (
            f" {high_priority_count} high-priority actions require immediate attention."
            if high_priority_count > 0
            else ""
        )

        date_desc = ""
        if metadata.dates:
            date_desc = f" Important dates: {metadata.dates[0]}."

        summary = (
            f"{doc_type_desc}{parties_desc} has been processed and classified."
            f"{financial_desc}{date_desc}{action_desc} The document has been categorized for"
            " appropriate workflow routing."
        )

        logger.info("%s: Summary generated (%s characters)", self.name, len(summary))
        return summary


class RiskAssessmentAgent:
    """Agent 5: Assesses risks and compliance."""

    def __init__(self):
        self.name = "RiskAssessmentAgent"
        logger.info("%s initialized", self.name)

    def assess_risks(self, metadata: DocumentMetadata, document_text: str) -> List[RiskAssessment]:
        """Assess risks based on document content."""
        logger.info("%s: Assessing risks", self.name)

        risks: List[RiskAssessment] = []
        text_lower = document_text.lower()

        if metadata.amounts:
            try:
                max_amount = max(
                    [float(a.replace("$", "").replace(",", "")) for a in metadata.amounts]
                )

                if max_amount > 50000:
                    risks.append(
                        RiskAssessment(
                            level="High",
                            description="High-value transaction requiring additional approval",
                            recommendation="Obtain executive approval before proceeding",
                        )
                    )
                elif max_amount > 10000:
                    risks.append(
                        RiskAssessment(
                            level="Medium",
                            description="Significant financial commitment",
                            recommendation="Verify budget allocation and obtain manager approval",
                        )
                    )
            except Exception:  # pragma: no cover - defensive
                logger.exception("Failed to parse monetary amounts for risk assessment")

        if metadata.doc_type == "Contract":
            risks.append(
                RiskAssessment(
                    level="Medium",
                    description="Legal agreement requiring compliance review",
                    recommendation="Complete legal checklist and obtain signatory approval",
                )
            )

        if metadata.dates and "urgent" in text_lower:
            risks.append(
                RiskAssessment(
                    level="High",
                    description="Time-sensitive document with approaching deadline",
                    recommendation="Fast-track through approval process",
                )
            )

        if "new vendor" in text_lower or "first time" in text_lower:
            risks.append(
                RiskAssessment(
                    level="Medium",
                    description="New vendor relationship",
                    recommendation="Complete vendor verification and due diligence",
                )
            )

        if not risks:
            risks.append(
                RiskAssessment(
                    level="Low",
                    description="Standard document with no unusual risk factors",
                    recommendation="Proceed with normal approval workflow",
                )
            )

        logger.info("%s: Identified %s risk factors", self.name, len(risks))
        return risks

