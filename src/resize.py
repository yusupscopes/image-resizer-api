import json
import boto3
import os
import io
from PIL import Image

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
    image = Image.open(io.BytesIO(image_bytes))

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
    for record in event["Records"]:
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]

        if not key.startswith("uploads/"):
            continue

        response = s3.get_object(Bucket=bucket, Key=key)
        image_bytes = response["Body"].read()

        resize_and_upload(image_bytes, key)

    return {
        "statusCode": 200,
        "body": json.dumps("Image resized successfully")
    }
