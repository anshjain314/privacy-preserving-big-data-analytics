import os

PROJECT_ROOT = "/media/sf_privacy_engine"

# Used by Python (os.makedirs, json.dump, etc.)
LOCAL_OUTPUT = os.path.join(PROJECT_ROOT, "outputs")

# Used by Spark .write.parquet()
SPARK_OUTPUT = "file:///media/sf_privacy_engine/outputs"