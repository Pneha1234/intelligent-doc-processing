"""
Agent evaluation utilities.
"""

from __future__ import annotations

import logging
from typing import Any, Dict

from .models import ProcessingResult

logger = logging.getLogger(__name__)


class AgentEvaluator:
    """Evaluation framework for measuring agent performance."""

    def __init__(self):
        self.metrics = {
            "total_processed": 0,
            "avg_processing_time": 0.0,
            "extraction_completeness": [],
        }
        logger.info("AgentEvaluator initialized")

    def evaluate_result(self, result: ProcessingResult):
        """Evaluate processing result and update metrics."""
        self.metrics["total_processed"] += 1

        times = [self.metrics["avg_processing_time"], result.processing_time_ms]
        self.metrics["avg_processing_time"] = sum(times) / len(times)

        extracted_fields = sum(
            [
                len(result.metadata.dates) > 0,
                len(result.metadata.amounts) > 0,
                len(result.metadata.parties) > 0,
                len(result.metadata.references) > 0,
            ]
        )
        completeness = extracted_fields / 4.0
        self.metrics["extraction_completeness"].append(completeness)

        logger.info(
            "Evaluation: Completeness=%.2f, Time=%sms",
            completeness,
            result.processing_time_ms,
        )

    def get_report(self) -> Dict[str, Any]:
        """Get evaluation report."""
        completeness_scores = self.metrics["extraction_completeness"]
        avg_completeness = (
            sum(completeness_scores) / len(completeness_scores)
            if completeness_scores
            else 0
        )

        return {
            "total_documents": self.metrics["total_processed"],
            "avg_processing_time_ms": round(self.metrics["avg_processing_time"], 2),
            "avg_extraction_completeness": round(avg_completeness, 2),
        }

