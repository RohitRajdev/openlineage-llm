import os
os.environ.setdefault("OPENLINEAGE_URL", "http://localhost:5000")
os.environ.setdefault("OPENLINEAGE_NAMESPACE", "ai-apps")
os.environ.setdefault("OPENLINEAGE_APP_NAME", "demo-llm")

from langchain_openai import ChatOpenAI
from openlineage_llm.integrations.langchain_callback import OpenLineageLangchainCallback

def main():
    llm = ChatOpenAI(model="gpt-4o-mini")  # requires OPENAI_API_KEY
    cb = OpenLineageLangchainCallback(job_name="demo.langchain.chat", inputs=["s3://docs/corpus"])
    resp = llm.invoke("Write a haiku about lineage.", config={"callbacks": [cb]})
    print(resp.content)

if __name__ == "__main__":
    main()
