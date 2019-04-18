import boto3, botocore
import os

S3_BUCKET = os.getenv('S3_BUCKET')
S3_ACCESS_KEY = os.getenv('S3_ACCESS_KEY')
S3_SECRET_KEY = os.getenv('S3_SECRET_KEY')
S3_LOCATION = f"https://{S3_BUCKET}.s3.amazonaws.com/"

SECRET_KEY = os.urandom(32)
DEBUG = True
PORT = 5000

s3 = boto3.client(
    "s3",
    aws_access_key_id=S3_ACCESS_KEY,
    aws_secret_access_key=S3_SECRET_KEY
)

def upload_to_s3( file, bucket_name, directory="", acl="public-read" ):
    directory_string = f"{S3_LOCATION}"

    if directory != "":
        directory_string += f"{directory}/"

    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            f'{directory}/{file.filename}',
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )
    except Exception as e:
        print("Something went wrong: ", e)
        return e
    

    return f"{directory_string}{file.filename}"
