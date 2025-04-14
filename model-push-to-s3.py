import os
import tarfile
import boto3
import dotenv
from new.serve import MODEL_FILE_NAME 
from new.serve import CONFIG_FILE_NAME
dotenv.load_dotenv('.env')
def compress_model(model_path):
    model_path = model_path.rstrip(os.sep)
    dir_name = os.path.dirname(model_path)
    base_name = os.path.basename(model_path)
    archive_file_name = f"{base_name}.tar.gz"
    archive_path = os.path.join(dir_name, archive_file_name)
    specific_model_file = os.path.join(model_path, MODEL_FILE_NAME)
    if not os.path.exists(specific_model_file):
        raise FileNotFoundError(f"{MODEL_FILE_NAME} not found in {model_path}")
    with tarfile.open(archive_path, 'w:gz') as tar:
        tar.add(specific_model_file, arcname=MODEL_FILE_NAME)
        config_file = os.path.join(model_path, CONFIG_FILE_NAME)
        if os.path.exists(config_file):
            tar.add(config_file, arcname=CONFIG_FILE_NAME)
        else:
            print(f"Warning: {CONFIG_FILE_NAME} not found in {model_path}")
    return archive_path
def push_model_to_s3(model_path, bucket_name='bucket-name'):
    """
    Compress the model directory and push the resulting tarball to the specified S3 bucket.
    Returns the S3 URI of the uploaded model.
    """
    s3 = boto3.client('s3')
    archive_path = compress_model(model_path)
    key = os.path.basename(archive_path)
    s3.upload_file(Filename=archive_path, Bucket=bucket_name, Key=key)
    model_uri = f"s3://{bucket_name}/{key}"
    return model_uri
if __name__ == "__main__":
    model_path = "your-model-path"
    bucket_name = "bucket-name"
    model_uri = push_model_to_s3(model_path, bucket_name)
    print("Model pushed to S3:", model_uri)
