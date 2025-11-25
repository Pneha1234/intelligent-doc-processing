"""
Data models used across the document processing system.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class DocumentMetadata:
    """Metadata extracted from documents."""

    doc_type: str
    confidence: float
    dates: List[str]
    amounts: List[str]
    parties: List[str]
    references: List[str]


@dataclass
class ActionItem:
    """Action item structure."""

    priority: str  # High, Medium, Low
    action: str
    assignee: str
    due_date: str | None = None


@dataclass
class RiskAssessment:
    """Risk assessment structure."""

    level: str  # High, Medium, Low
    description: str
    recommendation: str


@dataclass
class ProcessingResult:
    """Final processing result."""

    document_id: str
    timestamp: str
    metadata: DocumentMetadata
    action_items: List[ActionItem]
    summary: str
    risks: List[RiskAssessment]
    processing_time_ms: int

