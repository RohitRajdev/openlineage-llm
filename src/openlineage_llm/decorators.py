from __future__ import annotations
from functools import wraps
from typing import Callable, List, Optional, Dict, Any

from .client import OpenLineageExporter

def track_lineage(job_name: str, inputs: Optional[List[str]] = None, outputs: Optional[List[str]] = None, facets: Optional[Dict[str, Any]] = None):
    """Decorator to emit START/COMPLETE (or FAIL) around any Python function."""
    def wrapper(fn: Callable):
        @wraps(fn)
        def inner(*args, **kwargs):
            exporter = OpenLineageExporter()
            run_id = exporter.start(job_name=job_name, inputs=inputs or [], facets=facets or {})
            try:
                result = fn(*args, **kwargs)
                exporter.complete(job_name=job_name, run_id=run_id, outputs=outputs or [])
                return result
            except Exception as e:
                exporter.fail(job_name=job_name, run_id=run_id, error_message=str(e))
                raise
        return inner
    return wrapper
