# EvidenceOps

**Tagline:** Turn compliance and RFP questionnaires into cited, human-approved answer drafts.

> **MVP disclosure:** EvidenceOps is a review assistant, not a compliance certification service or an autonomous submission tool. It drafts from organization-supplied evidence, exposes gaps and conflicts, and requires human approval.

## Verified hackathon facts

Verified against the official Agents for Humans Hackathon pages on 2026-08-15:

- The submission period runs from August 10, 2026 at 9:00 AM PT through September 14, 2026 at 5:00 PM PT.
- The entry must be a new project created during the submission period. EvidenceOps was started on August 11, 2026.
- Strands Agents SDK is required. Amazon Bedrock AgentCore is optional and can strengthen the Technical Implementation score.
- The submission needs a public source repository containing the project source, an MIT or Apache license, a README, and an architecture diagram.
- The demonstration video must be publicly viewable and no longer than five minutes.
- An AWS Builder ID is required for participation.
- Five Stage Two criteria are equally weighted: Technical Implementation, Design, Potential Impact, Creativity and Originality, and Presentation.

Official sources: [overview](https://agentsforhumans.devpost.com/), [rules](https://agentsforhumans.devpost.com/rules), [dates](https://agentsforhumans.devpost.com/details/dates), and [FAQ](https://agentsforhumans.devpost.com/details/faqs).

Video upload, AWS Builder ID sign-in, registration, eligibility confirmation, and final submission remain project-owner actions.

**Development disclosure:** EvidenceOps was created during the submission period with implementation and documentation assistance from OpenAI Codex. It does not incorporate a pre-existing EvidenceOps product or private customer code.

## The problem

Security and compliance teams repeatedly answer long questionnaires for customers, partners, and procurement teams. The knowledge already exists across policies, audit reports, architecture documents, and previously approved answers, but finding the precise passage is slow. The costly part is not typing: it is proving that each claim is current, supported, internally consistent, and approved by the right person.

General-purpose text generation can make that problem worse. A fluent answer without a source is a liability. We built EvidenceOps around the opposite premise: uncertainty should become a visible work item, not confident prose.

## The solution

EvidenceOps takes a questionnaire in PDF, XLSX, or DOCX form plus a customer-controlled evidence library. It then runs a reviewable workflow:

1. Extract the questionnaire into traceable question records.
2. Retrieve relevant passages from the supplied evidence.
3. Draft an answer with source citations.
4. Check the draft for unsupported claims and conflicting evidence.
5. Produce a missing-evidence list when support is insufficient.
6. Send every item through a human approval queue.
7. Export approved answers with status, citations, gaps, and reviewer notes.

The product never treats generated text as evidence. When the evidence library cannot support a claim, EvidenceOps keeps the item blocked and describes what is needed.

## How we built it

The MVP uses the Strands Agents SDK for grounded drafting with typed structured output. A deterministic service coordinates question extraction, evidence retrieval, the Strands draft call, support checking, conflict detection, and gap classification. Deterministic application code retains ownership of file parsing, citation identity, workflow state, approval transitions, and export.

The release gate installs Strands Agents 1.52.0 with boto3 and botocore, then runs a credential-free
contract test through the real Strands `Agent`, OpenAI-compatible model adapter, typed output tool,
and EvidenceOps grounding workflow. The local endpoint fixture proves the SDK integration; it is not
presented as a third-party model-quality evaluation or Bedrock deployment.

Model calls pass through a provider abstraction configured with `BASE_URL`, `API_KEY`, and a model identifier. This supports an OpenAI-compatible endpoint for the demo while keeping the domain workflow independent of a single provider. The boundary applies request throttling, bounded retry, a circuit breaker, and an evidence-only deterministic fallback. After a provider failure, fallback text quotes retrieved evidence instead of improvising; when retrieval finds no evidence, the item remains blocked.

That provider is internal infrastructure: EvidenceOps never distributes model keys or exposes arbitrary prompt/chat proxying. The public demo defaults to the deterministic provider and synthetic evidence; switching on a non-demo provider is a separate operator decision.

The local-first MVP is designed for a clear AWS deployment path: Amazon S3 for encrypted documents and exports, DynamoDB for run and approval state, App Runner or ECS on Fargate for the service, OpenSearch Service or Knowledge Bases for Amazon Bedrock for larger-scale retrieval, Secrets Manager for provider credentials, CloudWatch for redacted telemetry, and an optional Amazon Bedrock model adapter.

See `docs/architecture.md` for the component diagram and the distinction between the implemented local MVP and optional managed-service deployment.

## Challenges we ran into

**Grounding at the claim level.** A retrieved paragraph may be related to a question without supporting the exact claim in a draft. We separated retrieval from verification and made citation presence, support status, and approval independent fields.

**Preserving questionnaire structure.** Spreadsheet cells and document sections are part of the buyer's expected deliverable, not incidental formatting. We retain source locations and question identifiers so drafts can be mapped back to export targets.

**Handling contradictions honestly.** Policies age at different rates. Silently choosing one source creates hidden risk, so the checker surfaces both passages and blocks the answer for a reviewer.

**Provider reliability.** Rate limits and transient failures should not erase work or encourage best-effort guessing. The adapter uses request throttling, bounded retries, a circuit breaker, and a deterministic evidence-only fallback.

**Keeping the human in control.** The interface needs to make evidence fast to inspect while ensuring a draft never looks approved by default. Approval is an explicit persisted transition and is invalidated by later edits.

## Accomplishments that we are proud of

- Built a complete MVP path from heterogeneous questionnaire ingestion to export.
- Made citations and missing evidence first-class workflow objects rather than annotations added at the end.
- Added contradiction and unsupported-claim review before approval.
- Preserved a human decision gate for every proposed answer.
- Kept provider-specific code behind an adapter with throttling and failure handling.
- Documented a practical AWS architecture without presenting future infrastructure as already deployed.
- Prepared an open-source release checklist, architecture package, and reproducible synthetic demo fixtures.

## What we learned

The most useful behavior for high-stakes document work is often a well-structured refusal to guess: identify the unsupported claim, show what was searched, and ask for a specific source. Citations also need stable document identity and locators; a model-generated footnote is not enough.

We also learned that human approval is not a final button bolted onto an agent. It changes the data model. Draft text, findings, review status, and reviewer notes need separate fields so the system can invalidate stale decisions and explain exactly what was exported.

Finally, a provider abstraction is valuable for more than portability. It provides one place to enforce rate limits, retries, a circuit breaker, and evidence-only fallback behavior across every drafting call.

## What's next

Before submission, we will run the synthetic evaluation set, capture the five-minute demonstration, and optionally deploy the same Strands service through Amazon Bedrock AgentCore to strengthen the Technical Implementation score. Any deployment will preserve the provider boundary, citation checks, and final human approval gate shown in the local MVP.

## Built with

- Python
- Strands Agents SDK
- OpenAI-compatible model API
- PDF, XLSX, and DOCX parsing
- Structured evidence retrieval and citations
- Human-in-the-loop review
- Amazon S3 (deployment path)
- Amazon DynamoDB (deployment path)
- AWS App Runner / Amazon ECS on AWS Fargate (deployment path)
- Amazon OpenSearch Service / Knowledge Bases for Amazon Bedrock (deployment path)
- AWS Secrets Manager and Amazon CloudWatch (deployment path)

## Suggested Devpost tags

`AI Agents` `Strands Agents` `AWS` `Compliance` `RFP Automation` `Human in the Loop` `Document AI` `Responsible AI` `Python` `Open Source`

## Links

- Hackathon: [Agents for Humans Hackathon](https://agentsforhumans.devpost.com/)
- Official rules: [Rules](https://agentsforhumans.devpost.com/rules)
- Official FAQ: [FAQ](https://agentsforhumans.devpost.com/details/faqs)
- Repository: https://github.com/FranklinNexus/evidenceops-agent
- Demo video: `PENDING-OWNER-ACTION: Upload the approved public video, then insert its URL.`
- Architecture: https://github.com/FranklinNexus/evidenceops-agent/blob/main/docs/architecture.md
- Devpost entry: `PENDING-OWNER-ACTION: Register or submit, then insert the project URL.`
