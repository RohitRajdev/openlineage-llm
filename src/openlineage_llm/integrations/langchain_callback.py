from __future__ import annotations
from typing import Any, Dict, List, Optional
from uuid import uuid4

try:
    from langchain_core.callbacks import BaseCallbackHandler
except Exception:  # Backward compat if different import path
    from langchain.callbacks.base import BaseCallbackHandler  # type: ignore

from ..client import OpenLineageExporter

class OpenLineageLangchainCallback(BaseCallbackHandler):
    """LangChain callback that emits OpenLineage START/COMPLETE around LLM/Chain runs."""
    def __init__(self, job_name: str, inputs: Optional[List[str]] = None):
        self.job_name = job_name
        self.inputs = inputs or []
        self._run_id: Optional[str] = None
        self._exporter = OpenLineageExporter()

    def _start(self, metadata: Dict[str, Any]):
        facets = {"langchain": {"_producer": "openlineage-llm", "metadata": metadata}}
        self._run_id = self._exporter.start(job_name=self.job_name, inputs=self.inputs, facets=facets)

    def _complete(self, outputs: Optional[List[str]] = None):
        if self._run_id:
            self._exporter.complete(job_name=self.job_name, run_id=self._run_id, outputs=outputs or [])

    # LLM-level
    def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any) -> None:
        meta = {"type": serialized.get("id"), "prompts": prompts[:1]}  # truncate for safety
        self._start(meta)

    def on_llm_end(self, response: Any, **kwargs: Any) -> None:
        self._complete()

    def on_llm_error(self, error: Exception, **kwargs: Any) -> None:
        if self._run_id:
            self._exporter.fail(job_name=self.job_name, run_id=self._run_id, error_message=str(error))

    # Chain-level (optional)
    def on_chain_start(self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any) -> None:
        meta = {"chain": serialized.get("id"), "inputs_keys": list(inputs.keys())}
        self._start(meta)

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        self._complete()

    def on_chain_error(self, error: Exception, **kwargs: Any) -> None:
        if self._run_id:
            self._exporter.fail(job_name=self.job_name, run_id=self._run_id, error_message=str(error))
