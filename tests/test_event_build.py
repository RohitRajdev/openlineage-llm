from openlineage_llm.events import job, run, dataset

def test_job_build():
    j = job("ns", "job1")
    assert j["namespace"] == "ns"
    assert j["name"] == "job1"

def test_run_build():
    r = run()
    assert "runId" in r

def test_dataset_build():
    d = dataset("ns", "s3://bucket/file.txt")
    assert d["name"].startswith("s3://")
