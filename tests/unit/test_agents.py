from document_processing.agents import DocumentClassifierAgent
from document_processing.session import MemoryBank


def test_classifier_detects_invoice():
    classifier = DocumentClassifierAgent(MemoryBank())

    doc_type, confidence = classifier.classify("This invoice is due next week.")

    assert doc_type == "Invoice"
    assert confidence >= 0.9


def test_classifier_handles_general_docs():
    classifier = DocumentClassifierAgent(MemoryBank())

    doc_type, confidence = classifier.classify("Random memo without keywords.")

    assert doc_type == "General Document"
    assert confidence == 0.70

