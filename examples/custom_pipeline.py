import os
os.environ.setdefault("OPENLINEAGE_URL", "http://localhost:5000")
os.environ.setdefault("OPENLINEAGE_NAMESPACE", "ai-apps")
os.environ.setdefault("OPENLINEAGE_APP_NAME", "demo-llm")

from openlineage_llm import track_lineage

@track_lineage(job_name="demo.custom.pipeline", inputs=["s3://bucket/raw.csv"], outputs=["s3://bucket/preds.parquet"])
def my_task(x):
    # Pretend to do something useful
    return x * 2

if __name__ == "__main__":
    print(my_task(21))
