from __future__ import annotations
import os
from pydantic import BaseModel

class Settings(BaseModel):
    openlineage_url: str = os.getenv("OPENLINEAGE_URL", "http://localhost:5000")
    namespace: str = os.getenv("OPENLINEAGE_NAMESPACE", "default")
    app_name: str = os.getenv("OPENLINEAGE_APP_NAME", "openlineage-llm")

settings = Settings()
