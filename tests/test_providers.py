from __future__ import annotations

from pathlib import Path

from evidenceops.config import Settings
from evidenceops.models import Citation
from evidenceops.providers import (
    AnswerProvider,
    DeterministicEvidenceProvider,
    DraftResult,
    ResilientProvider,
    StrandsBedrockProvider,
    StrandsOpenAIProvider,
    _validated_citation_indexes,
    build_provider,
)


class FailingProvider(AnswerProvider):
    name = "failing"

    def draft(self, question: str, citations: list[Citation]) -> DraftResult:
        raise RuntimeError("upstream unavailable")


def test_resilient_provider_falls_back_and_opens_circuit() -> None:
    citation = Citation(document="policy.txt", page_or_sheet="Lines 1-1", quote="MFA is enabled for administrators.")
    provider = ResilientProvider(
        FailingProvider(),
        DeterministicEvidenceProvider(),
        requests_per_minute=10,
        retries=0,
        failure_threshold=1,
        cooldown_seconds=60,
    )

    result = provider.draft("Is MFA enabled?", [citation])

    assert result.degraded is True
    assert result.provider == "deterministic-demo"
    assert provider.circuit_state == "open"
    assert citation.quote in result.answer


def test_provider_configuration_routes_without_external_calls() -> None:
    demo = build_provider(Settings(data_dir=Path("unused"), provider="auto"))
    assert isinstance(demo, DeterministicEvidenceProvider)

    openai = build_provider(
        Settings(
            data_dir=Path("unused"),
            provider="strands",
            base_url="https://HOST/v1",
            api_key="TOKEN",
            model="MODEL_ID",
        )
    )
    assert isinstance(openai, ResilientProvider)
    assert isinstance(openai.primary, StrandsOpenAIProvider)
    assert openai.primary.base_url == "https://HOST/v1"

    bedrock = build_provider(Settings(data_dir=Path("unused"), provider="bedrock", aws_region="us-east-1"))
    assert isinstance(bedrock, ResilientProvider)
    assert isinstance(bedrock.primary, StrandsBedrockProvider)
    assert bedrock.primary.region == "us-east-1"


def test_strands_citation_indexes_fail_closed() -> None:
    assert _validated_citation_indexes([1, 0, 1], 2) == [0, 1]

    for indexes in ([], [0, 2], [-1, 0]):
        try:
            _validated_citation_indexes(indexes, 2)
        except RuntimeError as exc:
            assert "invalid citation indexes" in str(exc)
        else:
            raise AssertionError(f"Expected invalid indexes to fail: {indexes}")
