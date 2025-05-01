import json
import boto3
import os
import io
import logging
from PIL import Image, UnidentifiedImageError

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client("s3")
BUCKET_NAME = os.environ.get("BUCKET_NAME", "")
RESIZED_PREFIX = "resized/"

# Define sizes
SIZES = {
    "thumbnail": (150, 150),
    "medium": (500, 500),
    "large": (1024, 768),
}

def resize_and_upload(image_bytes, original_key):
    buffer_image = io.BytesIO(image_bytes)
    buffer_image.seek(0)
    
    try:
        image = Image.open(buffer_image)
        image.verify()  # Check image integrity first
        buffer_image.seek(0)  # Rewind after verify, needed for thumbnailing
        image = Image.open(buffer_image).convert("RGB")
    except UnidentifiedImageError:
        logger.error(f"Unrecognized image format: {original_key}")
        return

    for label, size in SIZES.items():
        img_copy = image.copy()
        img_copy.thumbnail(size)

        buffer = io.BytesIO()
        img_copy.save(buffer, format="JPEG", optimize=True)
        buffer.seek(0)

        resized_key = f"{RESIZED_PREFIX}{label}/{original_key.split('/')[-1]}"
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=resized_key,
            Body=buffer,
            ContentType="image/jpeg"
        )

def handler(event, context):
    try:
        logger.info(f"Processing event: {json.dumps(event)}")
        for record in event["Records"]:
            bucket = record["s3"]["bucket"]["name"]
            key = record["s3"]["object"]["key"]

            if not key.startswith("uploads/"):
                continue
            
            if not key.lower().endswith((".jpg", ".jpeg", ".png")):
                logger.info(f"Skipping unsupported file: {key}")
                continue


            response = s3.get_object(Bucket=bucket, Key=key)
            logger.info(f"S3 object content type: {response.get('ContentType')}")
            image_bytes = response["Body"].read()

            resize_and_upload(image_bytes, key)

        return {
            "statusCode": 200,
            "body": json.dumps("Image resized successfully")
        }
    except Exception as e:
        logger.error(f"Error processing event: {str(e)}", exc_info=True)
        return {"statusCode": 500, "body": json.dumps({"message": "Error processing event!"})}
