from __future__ import annotations
from typing import Any, Dict, List, Optional

# LiteLLM supports callbacks via a callback manager API
# We implement a minimal interface compatible with litellm>=1.40

from ..client import OpenLineageExporter

class OpenLineageLiteLLMCallback:
    def __init__(self, job_name: str, inputs: Optional[List[str]] = None):
        self.job_name = job_name
        self.inputs = inputs or []
        self._run_id: Optional[str] = None
        self._exporter = OpenLineageExporter()

    def on_event_start(self, payload: Dict[str, Any]):
        model = payload.get("model")
        prompts = payload.get("messages", [])[:1]
        facets = {"litellm": {"_producer": "openlineage-llm", "model": model, "prompt": prompts}}
        self._run_id = self._exporter.start(job_name=self.job_name, inputs=self.inputs, facets=facets)

    def on_event_end(self, payload: Dict[str, Any]):
        self._exporter.complete(job_name=self.job_name, run_id=self._run_id, outputs=[])

    def on_event_error(self, error: Exception):
        if self._run_id:
            self._exporter.fail(job_name=self.job_name, run_id=self._run_id, error_message=str(error))
