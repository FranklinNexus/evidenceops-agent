# EvidenceOps

**Tagline:** No evidence, no answer. Turn compliance questionnaires into cited drafts with a human approval gate.

## Elevator pitch

EvidenceOps is the agent that knows when not to answer.

It turns a security, compliance, or RFP questionnaire plus an organization-controlled evidence library into cited answer drafts, contradiction findings, missing-evidence requests, a human review queue, and an exportable response set. Every factual answer must resolve to supplied evidence. Unsupported claims stay blocked.

EvidenceOps is for security, GRC, trust, and solutions engineering teams that must answer buyer questionnaires under deadline without weakening evidence discipline. It turns document search into an exception queue: supported drafts, source conflicts, and precise evidence requests, with a person deciding what leaves the system.

## Inspiration

Security questionnaires look like writing work, but the expensive part is evidence control. Teams repeatedly search policies, audit reports, architecture documents, and previously approved responses to prove that every statement is current and consistent.

A polished answer without a source is worse than a blank field: it can create contractual, audit, and trust risk. We built EvidenceOps around a simple operating principle: uploaded documents are evidence; generated text is not.

## What it does

EvidenceOps handles the questionnaire workflow end to end:

1. Ingest a questionnaire in PDF, XLSX, CSV, DOCX, Markdown, or text form.
2. Parse it into traceable question records with source locations.
3. Search only the uploaded evidence library for relevant passages.
4. Use a Strands agent to draft a concise answer with selected citation indexes.
5. Check the draft for unsupported claims, citation integrity, and conflicting evidence.
6. Turn missing support into a specific evidence request instead of plausible prose.
7. Require a person to approve, edit, or reject every answer.
8. Export approved work as XLSX, CSV, or JSON with citations and reviewer notes.

The application never distributes model credentials, exposes arbitrary prompt forwarding, or auto-submits an answer to a customer.

## What the working demo proves

The included synthetic CloudDesk review contains eight questions and four evidence documents. It deliberately exercises the cases that matter most:

- A supported encryption answer resolves to its exact source quote.
- Two incident-response documents disagree on a 48-hour versus 72-hour notification timeline. EvidenceOps shows both and blocks approval until a reviewer records a disposition.
- No current subprocessor register exists in the evidence pack. The item stays unanswered and becomes a missing-evidence request.
- Editing an approved answer clears the previous approval so stale sign-off cannot follow changed text.
- Approved-only export prevents drafts and unresolved items from being presented as final.

This is not a slideshow path. The repository includes the runnable Web workspace, API, synthetic fixtures, tests, architecture, and export implementation.

## How we built it

The MVP uses Python, FastAPI, SQLite, and the Strands Agents SDK. A reusable `EvidenceOpsService` coordinates parsing, evidence retrieval, grounded drafting, verification, workflow state, human review, and export.

Strands owns the model-assisted drafting step. Deterministic code owns the high-risk controls:

- document and citation identity;
- questionnaire structure and source locations;
- retrieval from the supplied evidence set;
- support and numeric-conflict checks;
- approval transitions and invalidation;
- missing-evidence classification; and
- approved-only export.

The Strands provider accepts a narrow typed `AgentDraft` result: answer text plus zero-based evidence indexes. Invalid or missing indexes fail closed. A release-gate integration test starts a local OpenAI-compatible protocol fixture and runs the real Strands `Agent`, `OpenAIModel`, typed output tool, retrieval, and grounding path end to end. It proves the SDK integration without presenting a fixture as hosted-model quality evidence.

## Reliability and provider boundary

Model access sits behind a provider abstraction supporting an operator-controlled OpenAI-compatible endpoint or Amazon Bedrock. The wrapper applies request throttling, bounded retry, a circuit breaker, and an evidence-only deterministic fallback.

If the provider is unavailable, fallback output may quote retrieved evidence but cannot improvise. If retrieval finds no support, the question remains blocked. The public demo defaults to synthetic evidence and the deterministic provider; activating a hosted provider is a separate operator decision.

The same service also exposes one restricted verification action through structured HTTP and an optional MCP adapter. It accepts a tenant-scoped project, question, proposed answer, and exact citations, then verifies every quote against stored project evidence. It is not a chat proxy. Tenant-separated limits, TTL caching, and metadata-only audit records apply.

## Challenges we ran into

### Retrieval is not proof

A passage can be related to a question without supporting every claim in a draft. We separated retrieval from grounding checks and made support status independent from model confidence.

### Contradictions should remain visible

Policies age at different rates. Automatically choosing the more convenient source would hide risk, so EvidenceOps preserves both conflicting passages and requires a reviewer disposition.

### Human approval changes the data model

Approval cannot be a decorative final button. Draft text, citations, checks, decision status, and reviewer notes are separate records. Any later answer edit invalidates the old approval.

### Provider failure must not become factual failure

Retries and fallback are useful only if fallback stays grounded. EvidenceOps degrades to evidence-only text or an explicit gap, never an uncited best guess.

## Accomplishments that we are proud of

- Built the complete loop from heterogeneous document upload to reviewable export.
- Made citations, conflicts, and missing evidence first-class workflow objects.
- Added a persisted human approval gate with approval invalidation after edits.
- Ran the real Strands SDK contract path in automated tests.
- Kept provider credentials and generic prompt proxying outside the public interface.
- Shipped a responsive review workspace, public MIT repository, synthetic fixtures, architecture package, and reproducible tests.
- Reached 88% application coverage with 28 passing tests.

## What we learned

For high-stakes document work, the most valuable agent behavior is often a structured refusal to guess: identify the unsupported claim, show what was searched, and ask for the exact missing source.

We also learned that trustworthy citations require stable document identity and locators. A generated footnote is not evidence. Finally, human review works best when it is part of the workflow state, not a disclaimer added after generation.

## What's next

The next technical step is an optional AWS deployment that preserves the same trust boundary: Amazon S3 for encrypted documents and exports, DynamoDB for workflow state, CloudWatch for redacted telemetry, and AgentCore or a container service for the Strands runtime. Larger evidence sets could move to OpenSearch Service or Knowledge Bases for Amazon Bedrock.

Production use would also add tenant authentication, role-based approval, malware scanning, retention controls, immutable audit logging, and organization-specific evaluation sets. These are future steps, not claims about the local MVP.

## Built with

- Python 3.11+
- Strands Agents SDK
- FastAPI and Pydantic
- SQLite
- OpenAI-compatible model adapter
- Amazon Bedrock adapter
- PDF, XLSX, CSV, and DOCX parsing
- HTML, CSS, and JavaScript review workspace
- pytest and pytest-cov
- Optional MCP transport
- AWS deployment path: AgentCore, S3, DynamoDB, CloudWatch, OpenSearch Service / Knowledge Bases for Amazon Bedrock

## Suggested tags

`AI Agents` `Strands Agents` `AWS` `Compliance` `RFP Automation` `Human in the Loop` `Document AI` `Responsible AI` `Python` `Open Source`

## Submission fields

| Field | Value |
| --- | --- |
| Project name | `EvidenceOps` |
| Track | `Professional Agents` |
| Repository | https://github.com/FranklinNexus/evidenceops-agent |
| Devpost thumbnail | `docs/assets/evidenceops-devpost-thumbnail.png` |
| Product image | `docs/assets/evidenceops-demo.png` |
| Architecture image | `docs/assets/evidenceops-architecture.png` |
| Architecture document | https://github.com/FranklinNexus/evidenceops-agent/blob/main/docs/architecture.md |
| Demo video | Add the final public YouTube or Vimeo URL; maximum 5:00 |
| Live demo | Optional; do not enter a localhost URL |
| AWS Builder ID | Project owner enters the identity-bound email |

## Disclosures

EvidenceOps was created during the 2026 Agents for Humans Hackathon submission period with implementation and documentation assistance from OpenAI Codex. It does not incorporate a pre-existing EvidenceOps product or private customer code. The demonstration fixtures are synthetic.

EvidenceOps assists document preparation. It is not a certification, audit opinion, legal determination, or autonomous submission system.

## Rule check

Verified against the official Agents for Humans Hackathon pages on 2026-08-17 (the rules page was updated on 2026-08-12):

- Submission deadline: September 14, 2026 at 5:00 PM PT, shown as September 15, 2026 at 8:00 AM GMT+8.
- Required: a new Strands project, public MIT or Apache repository, README, architecture diagram, public video no longer than five minutes, and AWS Builder ID.
- Amazon Bedrock AgentCore and a public live demo are optional.
- Submission materials must be in English or include an English translation.
- The optional builder.aws bonus no longer requires the `#AgentsforHumans` hashtag; the title must still include `Agents for Humans`.

Official sources: [overview](https://agentsforhumans.devpost.com/), [rules](https://agentsforhumans.devpost.com/rules), [dates](https://agentsforhumans.devpost.com/details/dates), and [FAQ](https://agentsforhumans.devpost.com/details/faqs).
