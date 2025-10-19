import os
os.environ.setdefault("OPENLINEAGE_URL", "http://localhost:5000")
os.environ.setdefault("OPENLINEAGE_NAMESPACE", "ai-apps")
os.environ.setdefault("OPENLINEAGE_APP_NAME", "demo-llm")

from litellm import completion
from openlineage_llm.integrations.litellm_callback import OpenLineageLiteLLMCallback

def main():
    cb = OpenLineageLiteLLMCallback(job_name="demo.litellm.chat", inputs=["s3://docs/corpus"])
    # LiteLLM docs show passing callbacks list; we simulate with manual calls for clarity
    cb.on_event_start({"model": "gpt-4o-mini", "messages": [{"role":"user","content":"hello lineage"}]})
    response = completion(model="gpt-4o-mini", messages=[{"role":"user","content":"hello lineage"}])
    cb.on_event_end({"response": response})

if __name__ == "__main__":
    main()
