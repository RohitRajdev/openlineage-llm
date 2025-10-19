from __future__ import annotations
import uuid
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime, timezone

@dataclass
class DatasetRef:
    name: str
    namespace: str

@dataclass
class Facets:
    # Simple facet container; can be extended to match OpenLineage facets schema.
    data: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RunEvent:
    eventType: str  # START or COMPLETE or FAIL
    eventTime: str
    run: Dict[str, Any]
    job: Dict[str, Any]
    inputs: List[Dict[str, Any]] = field(default_factory=list)
    outputs: List[Dict[str, Any]] = field(default_factory=list)
    producer: str = "https://github.com/your-org/openlineage-llm"

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def new_run_id() -> str:
    return str(uuid.uuid4())

def dataset(namespace: str, name: str, facets: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return {
        "namespace": namespace,
        "name": name,
        "facets": facets or {}
    }

def job(namespace: str, name: str, facets: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return {
        "namespace": namespace,
        "name": name,
        "facets": facets or {}
    }

def run(run_id: Optional[str] = None, facets: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return {
        "runId": run_id or new_run_id(),
        "facets": facets or {}
    }
