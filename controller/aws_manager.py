import os
import boto3

from dotenv import load_dotenv
from botocore.exceptions import ClientError

load_dotenv()


class AWSManager:

    def __init__(self):

        self.bucket_name = os.getenv("AWS_BUCKET_NAME")

        self.s3 = boto3.client(

            "s3",

            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),

            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),

            region_name=os.getenv("AWS_REGION")

        )

    def upload_file(self, local_path, s3_key):

        try:

            self.s3.upload_file(
                local_path,
                self.bucket_name,
                s3_key
            )

            print(f"✅ Uploaded {local_path} to S3")

            return True

        except ClientError as e:

            print(e)

            return False

    def list_files(self):

        response = self.s3.list_objects_v2(
            Bucket=self.bucket_name
        )

        if "Contents" not in response:

            print("Bucket is empty.")
            return

        print("\nFiles in Bucket:\n")

        for obj in response["Contents"]:

            print(obj["Key"])