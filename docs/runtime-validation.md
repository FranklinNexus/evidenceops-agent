# Runtime Validation

Validated on 2026-08-16 with Python 3.13.13.

## Installed release-gate dependencies

| Package | Version | Declared license |
| --- | --- | --- |
| `strands-agents` | 1.52.0 | Apache-2.0 |
| `boto3` | 1.43.72 | Apache-2.0 |
| `botocore` | 1.43.72 | Apache-2.0 |
| `openai` | 2.54.0 | Apache-2.0 |

`python -m pip check` reported no broken requirements.

The release environment uses `pip 26.2.1` and `pytest 9.1.1`. `pip-audit 2.10.1 --local`
reported no known vulnerabilities in the auditable installed packages; the unpublished local
`evidenceops 0.1.0` package was skipped because it is not present on PyPI.

## Reproducible Strands gate

Run:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_strands_integration.py -vv
```

The test starts a loopback OpenAI-compatible HTTP endpoint and then exercises:

1. `StrandsOpenAIProvider` constructing the installed Strands `OpenAIModel`.
2. A real Strands `Agent` invocation with the typed `AgentDraft` output tool.
3. An OpenAI-compatible chat-completions request containing the `AgentDraft` schema.
4. EvidenceOps retrieval, citation selection, deterministic grounding checks, and draft status.

This is a protocol and orchestration test using synthetic data. It does not claim that a hosted LLM,
Amazon Bedrock, or AgentCore was invoked, and it does not measure model quality. A hosted provider run
for the final video requires separately approved credentials and must keep those credentials off screen.

## Full suite result

```text
25 passed
85% application coverage
```
