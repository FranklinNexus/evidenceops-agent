# EvidenceOps: 5-Minute Demo Script

## Demo setup

Use a synthetic company evidence pack that contains no customer or production secrets. Prepare:

- one questionnaire with questions about encryption, access, incident response, resilience, penetration testing, AI use, and subprocessors;
- one current policy excerpt that supports an encryption answer;
- two deliberately conflicting incident-notification excerpts stating 48 and 72 hours;
- no subprocessor register, so the missing-evidence path is visible;
- at least one short answer that can be edited and approved; and
- a known export location that is empty before the run.

Before recording, use an operator-approved Strands provider with synthetic evidence and confirm that
the health view reports `strands-openai-compatible` or `strands-bedrock`. Keep every credential out of
the screen recording. Retain a completed deterministic synthetic run in a separate browser tab only
as recovery, and disclose it as precomputed fallback if used.

The Agents for Humans Hackathon requires a publicly viewable video no longer than five minutes. Target a finished cut of approximately 4:45 so title cards and encoding do not push the published duration over the limit. See the [official rules](https://agentsforhumans.devpost.com/rules).

## 0:00-0:25 - The problem

**On screen:** Start on the EvidenceOps workspace with no active run.

**Say:**

"No evidence, no answer. A security questionnaire looks like a writing task, but the real job is evidence control. Every answer needs a current source, conflicts need review, and missing proof must stay missing. EvidenceOps turns a questionnaire and an organization's own evidence into cited drafts, then keeps a human in charge of approval and export."

## 0:25-0:55 - Set the trust boundary

**On screen:** Show the upload areas for the questionnaire and evidence library.

**Say:**

"The boundary is deliberate: uploaded documents are evidence; generated text is not. Today I am using synthetic demo documents. EvidenceOps supports PDF, Excel, and Word inputs. It does not claim that a company has a control or certification unless a supplied source supports that statement."

**Action:** Upload the questionnaire and the evidence pack. Point to the filenames and source count.

## 0:55-1:30 - Start a run and extract questions

**On screen:** Start processing, then open the question list.

**Say:**

"The workflow extracts the questionnaire into traceable question records while retaining each original prompt and its source location. The agent then retrieves only the excerpts relevant to that record. That structure prevents one supporting passage from being stretched across unrelated claims."

**Action:** Show the eight-question queue, stable IDs, source filename, and saved pipeline counts.

## 1:30-2:20 - Retrieve evidence and draft with citations

**On screen:** Open the encryption question and its draft.

**Say:**

"For each requirement, EvidenceOps searches only the uploaded evidence library. This draft says what the policy supports, and the citation resolves to the exact source passage and locator. The draft is still unapproved. A citation is not decoration: the workflow separately checks whether the excerpt supports the actual claim."

**Action:** Show the cited encryption passage directly below the draft and point to its source locator.

**Say:**

"This run uses Strands Agents through a server-side provider boundary. The OpenAI-compatible and
Bedrock adapters apply throttling, bounded retries, a circuit breaker, and an evidence-only deterministic fallback. The
application never exposes a model key or arbitrary prompt proxy, and a failed provider call never
becomes an uncited answer."

## 2:20-3:10 - Surface a contradiction

**On screen:** Open the incident-notification question, which should show `CONFLICT`.

**Say:**

"This is a more important case than a polished answer. The evidence pack contains a current 48-hour incident notice and a legacy 72-hour timeline. EvidenceOps shows both excerpts instead of silently choosing one. The reviewer can identify the authoritative policy and record the decision."

**Action:** Expand both citations. Add a short disposition note, but leave the item unapproved long enough for the conflict status to remain clear.

## 3:10-3:55 - Turn missing proof into work

**On screen:** Open the subprocessor question and its missing-evidence warning.

**Say:**

"There is no current subprocessor register in this demo library. EvidenceOps does not invent one. It creates a specific evidence request tied to this question. That gives the team a concrete follow-up item while keeping the questionnaire honest."

**Action:** Show `NEEDS_REVIEW`, zero answer words, the missing-evidence warning, and no citation.

## 3:55-4:30 - Human review

**On screen:** Return to a supported draft.

**Say:**

"A person makes the final decision. I can edit this wording to match the response style, inspect the source again, and approve it. Approval is an explicit event. If I change the text afterward, the old approval is cleared so stale sign-off cannot follow a changed answer."

**Action:** Edit a supported answer, approve it, make a small second edit to demonstrate approval invalidation, then approve the final wording again.

## 4:30-4:50 - Export

**On screen:** Open the export view.

**Say:**

"By default, export includes only approved content. For this demo I can include drafts so the workbook also carries citations, missing evidence, reviewer notes, and decision status. Nothing is auto-submitted to the buyer."

**Action:** Enable **Include draft and rejected answers**, export XLSX, and open the result. Point to one approved answer and the unresolved subprocessor row.

## 4:50-5:00 - Close

**On screen:** Show the architecture diagram or return to the run summary.

**Say:**

"EvidenceOps is the agent that knows when not to answer. It makes evidence, uncertainty, and human approval part of one workflow, from upload to cited export, with a clear path to AgentCore and AWS-managed storage when the project is ready to deploy."

## Recording checklist

- [ ] The finished public video is no longer than 5:00; target approximately 4:45.
- [ ] Synthetic inputs are visibly labeled as demo data.
- [ ] The cited source passage is readable in the recording.
- [ ] At least one supported answer, one conflict, and one missing-evidence item are shown.
- [ ] An edit visibly invalidates approval before re-approval.
- [ ] The exported output is opened, not merely downloaded.
- [ ] No API key, local secret file, personal data, or customer evidence appears.
- [ ] Any precomputed fallback run is described accurately.
- [ ] No claim implies that optional AWS deployment components are already live.
- [ ] The final screen includes the project name and repository URL once publishing is approved.
