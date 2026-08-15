from __future__ import annotations

import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from evidenceops.config import Settings
from evidenceops.models import DocumentKind
from evidenceops.providers import StrandsOpenAIProvider
from evidenceops.service import EvidenceOpsService
from evidenceops.store import SQLiteStore


class _OpenAIContractHandler(BaseHTTPRequestHandler):
    requests: list[dict] = []

    def do_POST(self) -> None:  # noqa: N802 - stdlib handler API
        length = int(self.headers.get("content-length", "0"))
        body = self.rfile.read(length)
        request = json.loads(body)
        self.__class__.requests.append(request)
        if request.get("tools"):
            tool_name = request["tools"][0]["function"]["name"]
            message = {
                "role": "assistant",
                "content": None,
                "tool_calls": [
                    {
                        "id": "call-local-strands",
                        "type": "function",
                        "function": {
                            "name": tool_name,
                            "arguments": json.dumps(
                                {
                                    "answer": "Multi-factor authentication is required for administrators.",
                                    "citation_indexes": [0],
                                }
                            ),
                        },
                    }
                ],
            }
            finish_reason = "tool_calls"
        else:
            message = {
                "role": "assistant",
                "content": "Multi-factor authentication is required for administrators.",
            }
            finish_reason = "stop"
        response = {
            "id": "chatcmpl-local-strands",
            "object": "chat.completion",
            "created": 0,
            "model": "LOCAL_MODEL",
            "choices": [
                {
                    "index": 0,
                    "message": message,
                    "finish_reason": finish_reason,
                }
            ],
            "usage": {"prompt_tokens": 12, "completion_tokens": 12, "total_tokens": 24},
        }
        encoded = json.dumps(response).encode("utf-8")
        self.send_response(200)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def log_message(self, format: str, *args: object) -> None:
        del format, args


def test_strands_openai_provider_runs_through_evidenceops_service(tmp_path: Path) -> None:
    _OpenAIContractHandler.requests = []
    server = ThreadingHTTPServer(("127.0.0.1", 0), _OpenAIContractHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        settings = Settings(data_dir=tmp_path, provider="strands", retrieval_top_k=4)
        provider = StrandsOpenAIProvider(
            base_url=f"http://127.0.0.1:{server.server_port}/v1",
            api_key="LOCAL_TEST_TOKEN",
            model="LOCAL_MODEL",
        )
        store = SQLiteStore(tmp_path)
        service = EvidenceOpsService(store, provider, settings)
        project = store.create_project("Local Strands contract")
        service.upload_document(
            project.id,
            filename="security.md",
            data=b"Multi-factor authentication is required for administrators.",
            kind=DocumentKind.evidence,
            content_type="text/markdown",
        )
        service.add_manual_questions(project.id, ["Is multi-factor authentication required for administrators?"], None)

        result = service.run_project(project.id)

        assert result.processed == 1
        assert result.draft_count == 1
        question = result.questions[0]
        assert question.provider == "strands-openai-compatible"
        assert question.answer == "Multi-factor authentication is required for administrators."
        assert question.checks is not None and question.checks.grounded is True
        assert len(_OpenAIContractHandler.requests) == 1
        request = _OpenAIContractHandler.requests[0]
        assert request["model"] == "LOCAL_MODEL"
        assert request["stream"] is False
        assert request["tools"][0]["function"]["name"] == "AgentDraft"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)
