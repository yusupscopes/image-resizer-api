import boto3
import os
from fastapi import FastAPI, File, UploadFile
from mangum import Mangum
from uuid import uuid4
from src.metrics import publish_metric
import logging
import watchtower

s3 = boto3.client('s3')
BUCKET_NAME = os.environ.get("BUCKET_NAME", "")
UPLOAD_PREFIX = "uploads/"

app = FastAPI()

# Lambda entry point
handler = Mangum(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(watchtower.CloudWatchLogHandler(log_group='ImageUploadFunction'))

# Log requests and responses
@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response

# Upload image to S3
@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
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

    return {
        "message": "Image uploaded successfully",
        "original_key": file_key
    }
