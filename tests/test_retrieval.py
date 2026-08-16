from __future__ import annotations

from evidenceops.models import Citation, StoredChunk
from evidenceops.retrieval import analyze_grounding, retrieve


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


def test_grounding_rejects_unit_changes_and_cross_citation_claims() -> None:
    citations = [
        Citation(document="policy.md", page_or_sheet="Lines 1-3", quote="Backups are retained for 30 days."),
        Citation(document="incident.md", page_or_sheet="Lines 4-6", quote="Customers are notified within 48 hours."),
    ]

    changed_unit = analyze_grounding("Backups are retained for 30 hours.", citations)
    stitched = analyze_grounding("Backups are retained for 30 days and customers are notified within 48 hours.", citations)
    added_qualifier = analyze_grounding("All backups are retained for 30 days.", [citations[0]])

    assert changed_unit.grounded is False
    assert stitched.grounded is False
    assert added_qualifier.grounded is False


def test_grounding_rejects_new_relationship_built_across_sentences() -> None:
    citation = Citation(
        document="combined.md",
        page_or_sheet="Lines 1-4",
        quote="Customer data is encrypted at rest. Backups are retained for 30 days.",
    )

    result = analyze_grounding("Encrypted customer data is retained for 30 days.", [citation])

    assert result.grounded is False
    assert result.unsupported_claims == ["Encrypted customer data is retained for 30 days."]


def test_retrieval_requires_coverage_of_a_compound_question() -> None:
    transit_only = [
        _chunk("transit", "transport.md", "Customer data is encrypted in transit using TLS 1.2."),
    ]
    split_support = [
        *transit_only,
        _chunk("rest", "storage.md", "Customer data is encrypted at rest using AES-256."),
    ]
    question = "Is customer data encrypted in transit and at rest?"

    assert retrieve(question, transit_only) == []
    assert {citation.document for citation in retrieve(question, split_support)} == {"transport.md", "storage.md"}
