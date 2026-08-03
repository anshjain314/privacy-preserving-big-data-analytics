import os

from dotenv import load_dotenv

from utils import create_spark
from descriptive import descriptive_statistics
from fraud import fraud_analysis
from credit import credit_risk_analysis
from segmentation import customer_segmentation


# Explicitly load .env
load_dotenv("/media/sf_privacy_engine/.env")

BUCKET = os.getenv("AWS_BUCKET_NAME")

print("Bucket :", BUCKET)
print("Access Key Loaded :", os.getenv("AWS_ACCESS_KEY_ID") is not None)
print("Secret Key Loaded :", os.getenv("AWS_SECRET_ACCESS_KEY") is not None)

spark = create_spark()

print("\nLoading Protected Dataset From AWS S3...\n")

try:

    df = spark.read.csv(

        f"s3a://{BUCKET}/protected_dataset.csv",

        header=True,

        inferSchema=True

    )

    print("Dataset Loaded Successfully!")

except Exception as e:

    print("\nERROR:\n")
    print(repr(e))
    raise

print("\nRows :", df.count())
print("Columns :", len(df.columns))

print("\nRunning Spark Analytics...\n")

descriptive_statistics(df)

fraud_analysis(df)

credit_risk_analysis(df)

customer_segmentation(df)

print("\nAnalytics Pipeline Finished Successfully.\n")

spark.stop()