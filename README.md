[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17394175.svg)](https://doi.org/10.5281/zenodo.17394175)

[![ORCID](https://img.shields.io/badge/ORCID-0009--0009--6833--0050-brightgreen)](https://orcid.org/0009-0009-6833-0050)

# openlineage-llm — OpenLineage exporter for AI runs

Emit lineage events from **LangChain**, **LiteLLM**, or **custom pipelines** into **OpenLineage/Marquez**.
This brings **data engineering best practices** to LLM apps: auditable inputs/outputs, prompts, models,
and run-level metadata.

> Whitepaper: *Unifying Data & Model Lineage with Open Standards* (to be released on Zenodo).

## ✨ Features
- Send **RunStarted/RunCompleted** events to OpenLineage.
- Map **prompts, models, datasets** to OpenLineage inputs/outputs.
- **LangChain** and **LiteLLM** callbacks.
- **Decorator** for custom Python pipelines.
- Minimal config via environment variables.

## 🚀 Quickstart

### 1) Install
```bash
pip install -e .[langchain,litellm]
```

### 2) Configure
Set your OpenLineage backend and namespace (Marquez example):
```bash
export OPENLINEAGE_URL=http://localhost:5000
export OPENLINEAGE_NAMESPACE=ai-apps
export OPENLINEAGE_APP_NAME=demo-llm
```

### 3) Use with LangChain
```python
from langchain_openai import ChatOpenAI
from openlineage_llm.integrations.langchain_callback import OpenLineageLangchainCallback

llm = ChatOpenAI(model="gpt-4o-mini")
cb = OpenLineageLangchainCallback(job_name="demo.langchain.chat")

resp = llm.invoke("Write a haiku about lineage.", config={"callbacks": [cb]})
print(resp.content)
```

### 4) Use with LiteLLM
```python
from litellm import completion
from openlineage_llm.integrations.litellm_callback import OpenLineageLiteLLMCallback

cb = OpenLineageLiteLLMCallback(job_name="demo.litellm.chat")
response = completion(model="gpt-4o-mini", messages=[{"role":"user","content":"hello"}], callbacks=[cb])
```

### 5) Decorator for custom pipelines
```python
from openlineage_llm.decorators import track_lineage

@track_lineage(job_name="demo.custom.pipeline", inputs=["s3://bucket/raw.csv"], outputs=["s3://bucket/preds.parquet"])
def my_task(x):
    return x * 2

print(my_task(21))
```

## 🧱 Concepts & Mapping
- **Job**: `OPENLINEAGE_NAMESPACE.job_name`
- **Run**: `runId` created per call (uuid4)
- **Inputs**: datasets (e.g., prompt templates, embeddings index, documents URIs)
- **Outputs**: datasets (e.g., generated artifacts, cached results)
- **Facets**: prompt text (truncated), model name, tokens, cost, latency

## 📦 Repo Layout
```
openlineage-llm/
  src/openlineage_llm/
    __init__.py
    client.py
    config.py
    events.py
    decorators.py
    integrations/
      __init__.py
      langchain_callback.py
      litellm_callback.py
  examples/
    langchain_demo.py
    litellm_demo.py
    custom_pipeline.py
  tests/
    test_event_build.py
  .github/workflows/ci.yml
  pyproject.toml
  README.md
  LICENSE
  CITATION.cff
```

## 🧪 Testing
```bash
python -m pytest
```

## 🧭 Zenodo (DOI) — How-To
1. Create a **GitHub release** (e.g., `v0.1.0`).
2. Connect GitHub to **Zenodo**, enable archive for this repo.
3. Push a release — Zenodo will mint a **DOI**.
4. Upload the PDF whitepaper alongside the release assets.

## 📄 Whitepaper (outline)
- Introduction: Lineage for LLM-driven systems
- Standards: OpenLineage schema
- Architecture: callbacks + decorator + client
- Facet design: prompts/models/tokens
- Case studies: LangChain + LiteLLM
- Evaluation: overhead, visibility, reproducibility
- Discussion: governance & audit
- Conclusion / Future Work

---

**License:** MIT
