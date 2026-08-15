# Open-Source and Public-Repository Release Checklist

## Current project license

The repository currently contains the MIT License at the project root. Keep that license unless the maintainers deliberately choose Apache License 2.0 or an explicit dual-license model before publication. Do not describe the project as Apache-licensed while the repository contains only an MIT license file.

This checklist supports the public hackathon repository. It is an engineering release checklist, not legal advice.

## 1. Verified event requirements

The following requirements were verified against the official Agents for Humans Hackathon pages on 2026-08-15:

- [x] Submission is open from 2026-08-10 09:00 PT through 2026-09-14 17:00 PT.
- [x] The entry must be a new project created during the submission period.
- [x] Strands Agents SDK is required; Amazon Bedrock AgentCore is optional and can strengthen the Technical Implementation score.
- [x] The source repository must be public and include the project source, an MIT or Apache license, a README, and an architecture diagram.
- [x] The demonstration video must be publicly viewable and no longer than five minutes.
- [x] An AWS Builder ID is required for participation.
- [x] Technical Implementation, Design, Potential Impact, Creativity and Originality, and Presentation are equally weighted Stage Two judging criteria.
- [ ] Recheck the official pages immediately before publication and submission, and record the retrieval date in the release record.

Official sources: [overview](https://agentsforhumans.devpost.com/), [rules](https://agentsforhumans.devpost.com/rules), [dates](https://agentsforhumans.devpost.com/details/dates), and [FAQ](https://agentsforhumans.devpost.com/details/faqs).

Publication, hackathon registration, form submission, and external messaging require the project owner's explicit confirmation.

## 2. Choose and state one licensing model

### Option A: MIT (current repository)

- [ ] Keep the unmodified MIT text in root `LICENSE`.
- [ ] Confirm the copyright holder and year.
- [ ] State `MIT` in the README and package metadata.
- [ ] Preserve third-party MIT copyright and permission notices where required.

### Option B: Apache License 2.0

- [ ] Replace the root license only after an explicit maintainer decision.
- [ ] Include the complete, unmodified Apache License 2.0 text.
- [ ] State `Apache-2.0` in README and package metadata.
- [ ] Preserve applicable upstream `NOTICE` content and add a project `NOTICE` file when required.
- [ ] Review the patent-license and patent-termination provisions with the intended contributors.

### Option C: Dual MIT OR Apache-2.0

- [ ] Use explicit `MIT OR Apache-2.0` wording in package metadata and documentation.
- [ ] Include complete license texts, commonly as `LICENSE-MIT` and `LICENSE-APACHE`.
- [ ] Explain that recipients may choose either license; do not use ambiguous `MIT/Apache` wording.
- [ ] Confirm every contributor has agreed to license their contribution under both options.

For the current MVP, retaining the existing MIT license is the lowest-friction path unless verified event rules or contributor requirements dictate otherwise.

## 3. Source and dependency review

- [ ] Inventory direct and transitive production and development dependencies from the exact lock or environment used for the release.
- [ ] Record package name, version, source URL, license identifier, and notice obligations.
- [ ] Verify the exact installed Strands Agents SDK distribution and version; record its license from the authoritative package or repository.
- [ ] Verify licenses for PDF, XLSX, DOCX, web, test, and export libraries.
- [ ] Investigate missing, custom, source-available, copyleft, network-copyleft, noncommercial, or field-of-use licenses before release.
- [ ] Confirm copied snippets, templates, fonts, icons, screenshots, fixtures, and generated assets have documented provenance and redistribution rights.
- [ ] Preserve required attribution and license texts in `THIRD_PARTY_NOTICES` when applicable.
- [ ] Remove unused dependencies before generating the final inventory.

Useful Python checks, adapted to the project's environment:

```powershell
python -m pip install pip-licenses pip-audit
pip-licenses --format=json --with-urls --with-system > third-party-licenses.json
pip-audit
```

Treat scanner output as an inventory aid. Resolve `UNKNOWN` and nonstandard license results against the exact dependency source rather than assuming compatibility.

## 4. Repository sanitation

- [ ] Search tracked files and full Git history for API keys, tokens, passwords, private URLs, connection strings, cookies, and private keys.
- [ ] Rotate any exposed credential before publication; deleting the current file is not sufficient.
- [ ] Ensure `.env`, local databases, uploads, exports, logs, caches, virtual environments, and IDE files are ignored.
- [ ] Replace provider values with placeholders such as `BASE_URL`, `API_KEY`, and model-name examples.
- [ ] Remove client names, buyer questionnaires, proprietary policies, production prompts, and personal data.
- [ ] Use synthetic fixtures whose facts, entities, and citations are visibly fictional.
- [ ] Inspect screenshots and demo recordings for secrets, browser identity, notifications, and local paths.
- [ ] Check large or binary files for embedded metadata and redistribution restrictions.
- [ ] Review Git submodules, LFS objects, release artifacts, branches, and tags, not only the default branch.

Suggested read-only preflight checks:

```powershell
git status --short
git ls-files
git log --all --oneline --decorate
rg -n --hidden -g '!.git/**' '(API_KEY|SECRET|TOKEN|PASSWORD|BEGIN .*PRIVATE KEY)'
```

Use a dedicated secret scanner for the full history before making the repository public.

## 5. Required project disclosures

- [ ] README identifies the project as an MVP and describes the implemented path accurately.
- [ ] README contains setup, environment-variable, run, test, and demo-fixture instructions.
- [ ] README states that uploaded sources are evidence and generated drafts are not.
- [ ] README documents human approval before export and explains failure/fallback behavior.
- [ ] README distinguishes local implementation from optional AWS deployment architecture.
- [ ] Root `LICENSE` and package metadata use the same SPDX license identifier.
- [ ] `NOTICE` and `THIRD_PARTY_NOTICES` are included when dependency obligations require them.
- [ ] `SECURITY.md` provides a private vulnerability-reporting route that is ready to receive reports.
- [ ] `CONTRIBUTING.md` states contribution licensing, tests, and provenance expectations.
- [ ] The repository contains no claim of certification, guaranteed compliance, or autonomous buyer submission.

## 6. Provider and data disclosures

- [ ] Document that operators supply their own compatible provider endpoint and credentials.
- [ ] Document which document content is sent to a provider and at which workflow stages.
- [ ] Document request throttling, bounded retry, circuit-breaker, and deterministic fallback behavior.
- [ ] Confirm that no credential is logged, exported, committed, or used as evidence.
- [ ] Confirm provider terms permit the intended hackathon demo.
- [ ] State that data retention and training behavior depend on the operator's chosen provider and agreement.
- [ ] Verify optional AWS service claims against the deployed demo; label undeployed services as architecture or roadmap.

## 7. Reproducibility and supply chain

- [ ] Pin or lock dependencies sufficiently to reproduce the demo environment.
- [ ] Record the supported Python version and operating-system assumptions.
- [ ] Run unit/integration tests from a clean environment using only documented steps.
- [ ] Generate an SBOM, for example CycloneDX JSON or SPDX JSON, from the release environment.
- [ ] Run dependency vulnerability and license checks against the locked versions.
- [ ] Build artifacts from a clean checkout and record the commit ID.
- [ ] Avoid publishing local caches, model responses containing source content, or uploaded evidence inside container images.
- [ ] Pin GitHub Actions by trusted release or commit and grant minimum token permissions.
- [ ] Enable branch protection and required checks after repository publication if the hosting plan supports them.

## 8. Contribution and provenance policy

- [ ] Decide whether contributions use Developer Certificate of Origin sign-off, a CLA, or an explicit inbound-equals-outbound policy.
- [ ] State that contributors must have rights to submitted code, tests, prompts, fixtures, and media.
- [ ] Require disclosure of material copied or generated content where provenance or license terms apply.
- [ ] Do not accept real customer evidence as a test fixture.
- [ ] Record substantial third-party code modifications and retain upstream notices.
- [ ] Define maintainers who can approve releases and security fixes.

## 9. MIT/Apache compatibility notes

- MIT-licensed code can generally be included in an Apache-2.0 project when its copyright and permission notice are preserved.
- Apache-2.0 code includes conditions beyond the MIT text, including an express patent license and notice requirements for modified files and distributed `NOTICE` content when applicable.
- A project labeled only MIT should not absorb Apache-2.0 code and then distribute the combined work as though the MIT text were the only applicable condition. Preserve the Apache-2.0 terms and notices for that component and document the resulting distribution obligations.
- Dependency compatibility depends on the exact version, use, linking/distribution method, and license text. Package classifiers alone are not conclusive.
- Hosted APIs and model endpoints are governed by their service terms; they are not automatically covered by the repository's open-source license.

Escalate ambiguous licenses, copied proprietary material, patent-sensitive contributions, trademarks, or customer-data questions to qualified counsel before publication.

## 10. Public-release gate

Release only when every owner is recorded and each blocking item is closed.

| Gate | Evidence | Owner | Status |
| --- | --- | --- | --- |
| Event rules verified | Official URLs, captured wording, verified 2026-08-15 | `{{OWNER}}` | Verified; recheck before submission |
| Project license consistent | `LICENSE`, metadata, README | `{{OWNER}}` | `{{STATUS}}` |
| Dependencies cleared | Inventory, notices, exceptions | `{{OWNER}}` | `{{STATUS}}` |
| Secrets/history cleared | Scanner report and credential review | `{{OWNER}}` | `{{STATUS}}` |
| Fixtures/media cleared | Provenance register | `{{OWNER}}` | `{{STATUS}}` |
| Tests and clean build pass | CI or signed local report | `{{OWNER}}` | `{{STATUS}}` |
| Claims match implementation | README, demo, Devpost comparison | `{{OWNER}}` | `{{STATUS}}` |
| Publication approved | Explicit maintainer approval | `{{OWNER}}` | `{{STATUS}}` |

Final release record:

- Commit: `{{COMMIT_SHA}}`
- Version/tag: `{{VERSION}}`
- SBOM: `{{PATH_OR_URL}}`
- Third-party notices: `{{PATH_OR_URL}}`
- Test report: `{{PATH_OR_URL}}`
- Approval: `{{NAME_AND_DATE}}`
