import boto3
import os
from fastapi import FastAPI, File, UploadFile
from mangum import Mangum
from uuid import uuid4
from src.metrics import publish_metric
import logging
import json

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')
BUCKET_NAME = os.environ.get("BUCKET_NAME", "")
UPLOAD_PREFIX = "uploads/"

app = FastAPI()

# Lambda entry point
handler = Mangum(app)

# Upload image to S3
@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    try:
        logger.info(f"Processing file: {file}")
        file_extension = file.filename.split('.')[-1]
        file_key = f"{UPLOAD_PREFIX}{uuid4()}.{file_extension}"

        file_content = await file.read()

        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=file_key,
            Body=file_content,
            ContentType=file.content_type
        )

        publish_metric("ImageUploaded", 1)

        return {"statusCode": 200, "body": json.dumps({"message": "Image uploaded successfully!"})}
        
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}", exc_info=True)
        return {"statusCode": 500, "body": json.dumps({"message": "Error processing file!"})}
