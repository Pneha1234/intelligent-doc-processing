from document_processing.tools import DocumentParserTool


def test_extract_dates_and_amounts():
    text = "Invoice Date: 2025-11-25 Amount Due: $1,250.50"

    dates = DocumentParserTool.extract_dates(text)
    amounts = DocumentParserTool.extract_amounts(text)

    assert "2025-11-25" in dates
    assert "$1,250.50" in amounts


def test_extract_references():
    text = "Reference INV-9988 should match the purchase order PO-12345"

    references = DocumentParserTool.extract_references(text)

    assert "REF-9988" in references
    assert "REF-12345" in references

