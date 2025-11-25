from pathlib import Path

import pytest

from document_processing.orchestrator import DocumentProcessingOrchestrator


SAMPLES_DIR = Path(__file__).resolve().parents[1] / "sample_documents"


@pytest.fixture(scope="module")
def orchestrator():
    return DocumentProcessingOrchestrator()


def _read_sample(name: str) -> str:
    return (SAMPLES_DIR / name).read_text()


def test_invoice_pipeline(orchestrator):
    text = _read_sample("invoice_samples.txt")

    result = orchestrator.process_document(text, "INV_TEST")

    assert result.metadata.doc_type == "Invoice"
    assert result.metadata.amounts
    assert any(action.priority == "High" for action in result.action_items)


def test_contract_pipeline(orchestrator):
    text = _read_sample("contract_samples.txt")

    result = orchestrator.process_document(text, "CONTRACT_TEST")

    assert result.metadata.doc_type == "Contract"
    assert any(risk.level == "High" for risk in result.risks)


def test_edge_case_defaults_to_general_document(orchestrator):
    text = _read_sample("edge_cases.txt")

    result = orchestrator.process_document(text, "EDGE_TEST")

    assert result.metadata.doc_type in {"General Document", "Report"}
    # Even sparse docs should still produce at least one action item (archive).
    assert result.action_items

