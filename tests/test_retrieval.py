from __future__ import annotations

from evidenceops.models import StoredChunk
from evidenceops.retrieval import retrieve


def _chunk(identifier: str, document: str, text: str) -> StoredChunk:
    return StoredChunk(
        id=identifier,
        document_id=f"doc-{identifier}",
        document=document,
        page_or_sheet="Lines 1-20",
        text=text,
    )


def test_retrieval_requires_distinctive_topic_coverage_and_skips_headings() -> None:
    chunks = [
        _chunk(
            "security",
            "security.md",
            "## Encryption\nCustomer content is encrypted in transit with TLS 1.2 and encrypted at rest with AES-256.",
        ),
        _chunk(
            "privacy",
            "privacy.md",
            "## Data location\nCustomers select a United States or European Union storage region.",
        ),
    ]

    encryption = retrieve("Is customer data encrypted in transit and at rest?", chunks)
    location = retrieve("In which regions is customer data stored?", chunks)

    assert [citation.document for citation in encryption] == ["security.md"]
    assert encryption[0].quote.startswith("Customer content")
    assert [citation.document for citation in location] == ["privacy.md"]
    assert not location[0].quote.startswith("#")
