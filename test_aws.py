from controller.aws_manager import AWSManager

aws = AWSManager()

aws.upload_file(
    "outputs/protected_dataset.csv",
    "protected_dataset.csv"
)

aws.list_files()