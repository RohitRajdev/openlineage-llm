from __future__ import annotations
from typing import List, Dict, Any, Optional
import json
import requests

from .config import settings
from .events import RunEvent, now_iso, run as run_obj, job as job_obj, dataset as ds

class OpenLineageExporter:
    """Lightweight HTTP client to emit OpenLineage events to Marquez API."""

    def __init__(self, namespace: Optional[str] = None, app_name: Optional[str] = None, url: Optional[str] = None):
        self.url = (url or settings.openlineage_url).rstrip("/")
        self.namespace = namespace or settings.namespace
        self.app_name = app_name or settings.app_name

    # Marquez API expects POST /api/v1/lineage with event payloads
    def _post(self, payload: Dict[str, Any]) -> None:
        endpoint = f"{self.url}/api/v1/lineage"
        headers = {"Content-Type": "application/json"}
        resp = requests.post(endpoint, data=json.dumps(payload), headers=headers, timeout=10)
        resp.raise_for_status()

    def start(self, job_name: str, run_id: Optional[str] = None, inputs: Optional[List[str]] = None, facets: Optional[Dict[str, Any]] = None) -> str:
        rid = run_id or None
        run_body = run_obj(run_id=rid, facets=facets or {})
        payload = {
            "eventType": "START",
            "eventTime": now_iso(),
            "run": run_body,
            "job": job_obj(self.namespace, job_name, facets={"app": {"_producer": "openlineage-llm", "appName": self.app_name}}),
            "inputs": [ds(self.namespace, name) for name in (inputs or [])],
            "outputs": [],
            "producer": "https://github.com/your-org/openlineage-llm",
        }
        self._post(payload)
        return run_body["runId"]

    def complete(self, job_name: str, run_id: str, outputs: Optional[List[str]] = None, facets: Optional[Dict[str, Any]] = None) -> None:
        payload = {
            "eventType": "COMPLETE",
            "eventTime": now_iso(),
            "run": {"runId": run_id, "facets": facets or {}},
            "job": job_obj(self.namespace, job_name),
            "inputs": [],
            "outputs": [ds(self.namespace, name) for name in (outputs or [])],
            "producer": "https://github.com/your-org/openlineage-llm",
        }
        self._post(payload)

    def fail(self, job_name: str, run_id: str, error_message: str) -> None:
        payload = {
            "eventType": "FAIL",
            "eventTime": now_iso(),
            "run": {"runId": run_id, "facets": {"errorMessage": {"message": error_message}}},
            "job": job_obj(self.namespace, job_name),
            "inputs": [],
            "outputs": [],
            "producer": "https://github.com/your-org/openlineage-llm",
        }
        self._post(payload)
