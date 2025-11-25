"""
Entry point for running the document processing orchestrator locally or via ADK.
"""

from __future__ import annotations

import logging
from typing import Iterable, Tuple

from document_processing import AgentEvaluator, DocumentProcessingOrchestrator
from document_processing.adk_app import DocumentProcessingADKApp

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def print_result(result):
    """Pretty-print helper for CLI demo output."""
    print(f"\n✅ Document Type: {result.metadata.doc_type}")
    print(f"📊 Confidence: {result.metadata.confidence * 100:.1f}%")
    print(f"⏱️  Processing Time: {result.processing_time_ms}ms")
    print(f"\n📝 Summary:\n{result.summary}")
    print(f"\n✓ Action Items: {len(result.action_items)}")
    for action in result.action_items:
        print(f"  • [{action.priority}] {action.action} → {action.assignee}")
    print(f"\n⚠️  Risks: {len(result.risks)}")
    for risk in result.risks:
        print(f"  • [{risk.level}] {risk.description}")


def run_demo(
    orchestrator: DocumentProcessingOrchestrator,
    documents: Iterable[Tuple[str, str]],
):
    """Run a quick CLI demo to mirror the original script."""
    evaluator = AgentEvaluator()

    for idx, (doc_id, content) in enumerate(documents, start=1):
        print(f"\n📄 Processing Document {idx}: {doc_id}")
        print("-" * 80)
        result = orchestrator.process_document(content, doc_id)
        evaluator.evaluate_result(result)
        print_result(result)
        print("\n" + "=" * 80)

    report = evaluator.get_report()
    print("📈 EVALUATION REPORT")
    print("=" * 80)
    for key, value in report.items():
        print(f"{key}: {value}")


def main():
    orchestrator = DocumentProcessingOrchestrator()

    sample_docs = [
        (
            "DOC001",
            """
            INVOICE
            Invoice Number: INV-2025-001
            Date: November 25, 2025
            Due Date: December 15, 2025

            From: Global Solutions Inc
            To: Acme Corp

            Description: Professional Services - Q4 2025
            Amount: $15,000.00
            Tax: $2,500.00
            Total: $17,500.00

            Payment Terms: Net 30 days
            Reference: PO-45678

            Please remit payment to the address below.
            """,
        ),
        (
            "DOC002",
            """
            SERVICE AGREEMENT

            This agreement is entered into on November 25, 2025
            between Tech Innovations LLC and Enterprise Solutions Corp

            Terms and Conditions:
            - Contract Value: $125,000
            - Duration: 12 months
            - Payment Schedule: Quarterly
            - Reference: CONTRACT-2025-Q4-089

            This is a new vendor relationship requiring compliance review.
            URGENT: Signature required by December 1, 2025
            """,
        ),
    ]

    run_demo(orchestrator, sample_docs)

    # Initialize ADK agent so the same pipeline can be used via `adk web`.
    adk_app = DocumentProcessingADKApp()
    logger.info(
        "ADK agent initialized. Launch with: adk web document_processing/adk_app.py:DocumentProcessingADKApp"
    )


if __name__ == "__main__":
    main()

