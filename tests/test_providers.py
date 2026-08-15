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
