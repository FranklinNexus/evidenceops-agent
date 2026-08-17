# Open-Source Release Record

Verified on 2026-08-17 for the public Agents for Humans Hackathon repository.

## Repository and license

- Public repository: https://github.com/FranklinNexus/evidenceops-agent
- Default branch: `main`
- License: MIT in root `LICENSE`, package metadata, and README
- GitHub license detection: MIT
- Public materials: source, synthetic fixtures, setup instructions, architecture, product image, and validation notes

The project uses only synthetic CloudDesk fixtures. It contains no customer questionnaires, private
policies, model credentials, generic prompt proxy, or client-accessible provider key.

## Reproducibility gate

Validated with Python 3.13.13:

```text
28 passed
88% application coverage
pip check: no broken requirements
pip-audit --local: no known vulnerabilities in auditable installed packages
wheel build: passed
```

The dedicated Strands integration test instantiates the installed Strands `Agent` and
`OpenAIModel`, sends a typed `AgentDraft` tool schema through a loopback OpenAI-compatible protocol
fixture, and carries the result through EvidenceOps retrieval, citation binding, grounding, and
workflow state. This verifies the SDK and orchestration path. It does not claim hosted-model,
Amazon Bedrock, or AgentCore inference quality.

Recorded release-gate packages:

| Package | Version | Declared license |
| --- | --- | --- |
| `strands-agents` | 1.52.0 | Apache-2.0 |
| `boto3` | 1.43.72 | Apache-2.0 |
| `botocore` | 1.43.72 | Apache-2.0 |
| `openai` | 2.54.0 | Apache-2.0 |

See `docs/runtime-validation.md` for commands and scope.

## Sanitation gate

- `.env`, databases, uploads, exports, logs, caches, build output, and virtual environments are ignored.
- Current tracked files and all reachable commits were scanned for high-confidence private keys and common token formats; no matches were found.
- Provider examples use `BASE_URL`, `API_KEY`, `MODEL_ID`, and synthetic local-test values.
- Screenshots contain synthetic product data and no keys, local paths, notifications, or customer data.
- Devpost copy discloses Codex assistance and distinguishes implemented behavior from optional AWS architecture.

## Claim boundary

- Uploaded organization-controlled documents are evidence; generated text is not.
- Every draft carries citations and must pass deterministic support checks before approval.
- Missing support becomes an evidence request, not a fabricated answer.
- Conflicting evidence stays visible for reviewer disposition.
- Human approval is persisted and invalidated after answer edits or new evidence.
- Exports include approved answers by default.
- Amazon Bedrock, AgentCore, S3, DynamoDB, CloudWatch, OpenSearch, and Knowledge Bases are documented as an optional deployment path, not as deployed services.

## Remaining submission actions

- Publish the final public YouTube or Vimeo demo at no more than five minutes.
- Enter the project owner's country, submitter type, and AWS Builder ID on Devpost.
- Recheck eligibility and every public URL, then have the project owner perform the final Submit action before 2026-09-14 17:00 PT.
