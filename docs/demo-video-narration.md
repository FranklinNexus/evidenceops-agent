# EvidenceOps demo video narration

This document records the disclosure and scene outline for `scripts/generate_demo_video.py`; the generator is the
source of truth for the exact English narration. The rendered video uses only the
synthetic fixtures under `examples/`, local UI captures, the generated XLSX export, and repository-owned diagrams.

The video deliberately says that:

- the recorded workspace runs locally with the deterministic evidence-only provider;
- the Strands release gate uses the installed SDK and a loopback OpenAI-compatible protocol fixture;
- the release gate proves integration, not hosted-model quality;
- Amazon Bedrock, AgentCore, and the wider AWS architecture are future deployment options, not live services; and
- every organization-specific statement shown in the demo comes from fictional CloudDesk fixtures.

## Scene outline

1. **EvidenceOps** - The agent that knows when not to answer.
2. **Trust boundary** - Synthetic questionnaire and organization-controlled evidence library.
3. **Agent run** - Extract, retrieve, draft, verify, and classify gaps.
4. **Cited answer** - Encryption claim and its exact source passage.
5. **Conflict** - Current 48-hour language versus a superseded 72-hour plan.
6. **Missing evidence** - No subprocessor register, answer, or citation.
7. **Human approval** - Supported MFA draft becomes approved.
8. **Approval invalidation** - Editing clears the old decision and requires re-approval.
9. **Export** - XLSX, CSV, or JSON, approved-only by default.
10. **Workbook** - Answers, status, citations, and evidence requests remain together.
11. **Architecture** - Strands drafting inside deterministic controls and a human gate.
12. **Strands gate** - Real SDK path against a loopback protocol fixture.
13. **Close** - Working local stack and clearly labeled optional AWS path.

## Reproduce

Run the local application and capture the UI states described in `docs/demo-script.md`, then generate the XLSX
demo export. With `edge-tts`, `imageio-ffmpeg`, Pillow, and openpyxl installed in the active Python environment:

```powershell
python scripts\generate_demo_video.py
```

The generator writes:

- `outputs/evidenceops-demo-video.mp4`
- `outputs/evidenceops-demo-video.en.srt`

The final script checks the encoded duration and fails if it exceeds five minutes.
