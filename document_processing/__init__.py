"""
Document processing package that exposes the primary orchestrator and ADK
integration helpers.
"""

from .config import settings
from .models import (
    DocumentMetadata,
    ActionItem,
    RiskAssessment,
    ProcessingResult,
)
from .orchestrator import DocumentProcessingOrchestrator
from .evaluation import AgentEvaluator

__all__ = [
    "settings",
    "DocumentMetadata",
    "ActionItem",
    "RiskAssessment",
    "ProcessingResult",
    "DocumentProcessingOrchestrator",
    "AgentEvaluator",
]

