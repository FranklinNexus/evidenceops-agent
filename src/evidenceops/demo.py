from __future__ import annotations

from pathlib import Path


DEMO_QUESTIONNAIRE = "questionnaire.csv"
DEMO_EVIDENCE = (
    "business-continuity.md",
    "legacy-incident-plan.md",
    "privacy-and-ai.md",
    "security-overview.md",
)


def demo_files() -> tuple[tuple[str, bytes], list[tuple[str, bytes]]]:
    package_root = Path(__file__).resolve().parent / "examples"
    repository_root = Path(__file__).resolve().parents[2] / "examples"
    root = next((candidate for candidate in (package_root, repository_root) if candidate.is_dir()), None)
    if root is None:
        raise FileNotFoundError("Synthetic demo fixtures are not installed")

    questionnaire = (DEMO_QUESTIONNAIRE, (root / DEMO_QUESTIONNAIRE).read_bytes())
    evidence = [(name, (root / "evidence" / name).read_bytes()) for name in DEMO_EVIDENCE]
    return questionnaire, evidence
