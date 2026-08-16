# Agents for Humans Hackathon Compliance

Verified against the official Devpost pages on 2026-08-16. The event remains open, Devpost shows
2,416 participants, and the project gallery has not yet been published, so a current public
submission count is not available.

## Official timeline

- Submission period: 2026-08-10 09:00 PT through 2026-09-14 17:00 PT.
- Submission deadline in China Standard Time: 2026-09-15 08:00 GMT+8.
- Judging period: 2026-09-15 09:00 PT through 2026-10-08 17:00 PT.
- Winners announced: on or around 2026-10-14 14:00 PT.
- Optional $50 AWS credit request deadline: 2026-09-11 12:00 PT, while supplies last. Credits expire 2026-10-31.

## Eligibility and build rules

- Entrants may be eligible individuals, teams, or organizations; individuals must be at least the age of majority where they reside.
- Entrant residence and organization domicile must be checked against the excluded locations in the full rules before registration.
- The project must be newly created during the submission period. This repository was started on 2026-08-11.
- The agent must use Strands Agents SDK and do real work end to end, rather than only chat about a task.
- An AWS Builder ID is required for participation.
- The official FAQ says an AWS account is required to participate. AgentCore is encouraged but optional; Strands Agents is the required foundation.
- The rules page was updated on 2026-08-12 to remove the `#AgentsforHumans` requirement from the optional blog-post bonus.
- Third-party code, SDKs, APIs, and data must be used under their applicable terms and licenses.
- All submission materials must be in English or include English translations.

## EvidenceOps submission mapping

| Official requirement | Repository evidence | Status |
| --- | --- | --- |
| New agent using Strands Agents SDK | `src/evidenceops/`, dependency manifest, and `tests/test_strands_integration.py` | Complete locally |
| Complete working project | Web app, API, local fallback, tests | Complete locally |
| Text description | `docs/devpost.md` | In progress |
| Public repository URL | https://github.com/FranklinNexus/evidenceops-agent | Complete; public MIT repository verified |
| All source, assets, and setup instructions | Repository plus `README.md` | Complete locally |
| MIT or Apache license | `LICENSE` (MIT) | Complete locally |
| README | `README.md` | Complete locally |
| Architecture diagram | `docs/architecture.md` and `docs/assets/evidenceops-architecture.png` | Complete locally |
| Public YouTube/Vimeo video, maximum 5 minutes | `docs/demo-script.md` is the recording plan | Recording and publication required |
| Video demonstrates working project | Script covers the full evidence-to-export flow | In progress |
| Pitch covers problem, audience, and importance | Devpost copy and demo script | In progress |
| AWS Builder ID | Not collected | User action required |
| Optional live demo | Local demo only | Deployment decision required |
| AWS account | Required by official FAQ | User action required |
| Optional builder.aws post with `Agents for Humans` in the title | Not published | Optional; do not delay submission |

## Judging alignment

The five Stage Two criteria are equally weighted:

1. Technical Implementation: genuine, non-trivial use of Strands Agents; a live demo and/or AgentCore deployment strengthens the score.
2. Design: a complete and coherent product experience.
3. Potential Impact: a credible solution to a specific real-world problem for a real audience.
4. Creativity and Originality: a non-obvious use of Strands with demonstrated domain understanding.
5. Presentation: a clear end-to-end demonstration and pitch.

Optional public builder.aws posts can add 0.2 points each, up to 0.6 total, when published before
the deadline. The official rules were updated on 2026-08-12 to remove the
`#AgentsforHumans` requirement; current overview language asks for `Agents for Humans` in the title.

## Actions deliberately not performed

- Devpost registration or submission.
- AWS credit request.
- Final Devpost submission.
- AWS deployment or creation of paid resources.
- Uploading or publishing the demo video or builder.aws post.

Identity and final-submission actions remain with the project owner.

## Official sources

- Overview and requirements: https://agentsforhumans.devpost.com/
- Full rules: https://agentsforhumans.devpost.com/rules
- Schedule: https://agentsforhumans.devpost.com/details/dates
- FAQs: https://agentsforhumans.devpost.com/details/faqs
- Strands quickstart linked by the rules: https://strandsagents.com/docs/user-guide/quickstart/overview/
