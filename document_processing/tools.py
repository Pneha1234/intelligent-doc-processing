"""
Custom tools used for document parsing and entity extraction.
"""

from __future__ import annotations

import logging
import re
from typing import List

logger = logging.getLogger(__name__)


class DocumentParserTool:
    """Custom tool for parsing document content."""

    @staticmethod
    def extract_dates(text: str) -> List[str]:
        """Extract dates from text."""
        date_patterns = [
            r"\d{4}-\d{2}-\d{2}",  # YYYY-MM-DD
            r"\d{2}/\d{2}/\d{4}",  # MM/DD/YYYY
            r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}",
        ]
        dates: List[str] = []
        for pattern in date_patterns:
            dates.extend(re.findall(pattern, text, re.IGNORECASE))
        logger.debug("Extracted %s dates", len(dates))
        return dates

    @staticmethod
    def extract_amounts(text: str) -> List[str]:
        """Extract monetary amounts from text."""
        amount_pattern = r"\$[\d,]+(?:\.\d{2})?"
        amounts = re.findall(amount_pattern, text)
        logger.debug("Extracted %s amounts", len(amounts))
        return amounts

    @staticmethod
    def extract_references(text: str) -> List[str]:
        """Extract reference numbers (invoice #, PO #, etc.)."""
        ref_patterns = [
            r"(?:INV|Invoice)[-#]?\s*(\d+)",
            r"(?:PO|Purchase Order)[-#]?\s*(\d+)",
            r"(?:REF|Reference)[-#]?\s*([A-Z0-9-]+)",
        ]
        references: List[str] = []
        for pattern in ref_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            references.extend([f"REF-{m}" for m in matches])
        logger.debug("Extracted %s references", len(references))
        return references


class EntityExtractionTool:
    """Tool for extracting named entities."""

    @staticmethod
    def extract_parties(text: str) -> List[str]:
        """Extract company/party names."""
        keywords = ["Inc", "LLC", "Corp", "Corporation", "Ltd", "Limited"]
        lines = text.split("\n")
        parties: List[str] = []

        for line in lines:
            for keyword in keywords:
                if keyword in line:
                    words = line.split()
                    for i, word in enumerate(words):
                        if keyword in word:
                            company = " ".join(words[max(0, i - 3) : i + 1])
                            parties.append(company.strip())
                            break

        logger.debug("Extracted %s parties", len(parties))
        return list(set(parties))  # Remove duplicates

