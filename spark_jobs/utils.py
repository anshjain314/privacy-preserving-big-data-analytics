import os
from pyspark.sql import SparkSession


def create_spark():

    spark = (
        SparkSession.builder
        .appName("PrivacyPreservingAnalytics")

        .config(
            "spark.hadoop.fs.s3a.impl",
            "org.apache.hadoop.fs.s3a.S3AFileSystem"
        )

        .config(
            "spark.hadoop.fs.s3a.endpoint",
            "s3.eu-north-1.amazonaws.com"
        )

        .config(
            "spark.hadoop.fs.s3a.access.key",
            os.getenv("AWS_ACCESS_KEY_ID")
        )

        .config(
            "spark.hadoop.fs.s3a.secret.key",
            os.getenv("AWS_SECRET_ACCESS_KEY")
        )

        .config(
            "spark.hadoop.fs.s3a.aws.credentials.provider",
            "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider"
        )

        .config(
            "spark.hadoop.fs.s3a.path.style.access",
            "false"
        )

        .config(
            "spark.hadoop.fs.s3a.connection.ssl.enabled",
            "true"
        )

        .getOrCreate()
    )

    return spark