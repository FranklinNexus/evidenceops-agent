from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _int_env(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except ValueError:
        return default


def _float_env(name: str, default: float) -> float:
    try:
        return float(os.getenv(name, str(default)))
    except ValueError:
        return default


@dataclass(slots=True)
class Settings:
    data_dir: Path
    provider: str = "auto"
    base_url: str = "http://localhost:8001/v1"
    api_key: str = ""
    model: str = "MODEL_ID"
    aws_region: str = "us-west-2"
    bedrock_model: str = "MODEL_ID"
    max_upload_mb: int = 20
    requests_per_minute: int = 30
    provider_retries: int = 2
    circuit_failure_threshold: int = 3
    circuit_cooldown_seconds: float = 30.0
    retrieval_top_k: int = 4
    tool_calls_per_minute: int = 60
    tool_cache_ttl_seconds: float = 300.0

    @classmethod
    def from_env(cls) -> "Settings":
        base_url = os.getenv("OPENAI_COMPATIBLE_BASE_URL") or os.getenv("OPENAI_BASE_URL")
        api_key = os.getenv("OPENAI_COMPATIBLE_API_KEY") or os.getenv("OPENAI_API_KEY")
        return cls(
            data_dir=Path(os.getenv("EVIDENCEOPS_DATA_DIR", "data")),
            provider=os.getenv("EVIDENCEOPS_PROVIDER", "auto").lower(),
            base_url=base_url or "http://localhost:8001/v1",
            api_key=api_key or "",
            model=os.getenv("OPENAI_COMPATIBLE_MODEL", os.getenv("OPENAI_MODEL", "MODEL_ID")),
            aws_region=os.getenv("AWS_REGION", "us-west-2"),
            bedrock_model=os.getenv("BEDROCK_MODEL_ID", "MODEL_ID"),
            max_upload_mb=_int_env("EVIDENCEOPS_MAX_UPLOAD_MB", 20),
            requests_per_minute=_int_env("EVIDENCEOPS_REQUESTS_PER_MINUTE", 30),
            provider_retries=_int_env("EVIDENCEOPS_PROVIDER_RETRIES", 2),
            circuit_failure_threshold=_int_env("EVIDENCEOPS_CIRCUIT_FAILURE_THRESHOLD", 3),
            circuit_cooldown_seconds=_float_env("EVIDENCEOPS_CIRCUIT_COOLDOWN_SECONDS", 30.0),
            retrieval_top_k=_int_env("EVIDENCEOPS_RETRIEVAL_TOP_K", 4),
            tool_calls_per_minute=_int_env("EVIDENCEOPS_TOOL_CALLS_PER_MINUTE", 60),
            tool_cache_ttl_seconds=_float_env("EVIDENCEOPS_TOOL_CACHE_TTL_SECONDS", 300.0),
        )
