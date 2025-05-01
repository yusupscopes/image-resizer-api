# Image Resizer & Optimizer API

Automatically resize and compress user-uploaded images to optimize performance using a serverless architecture on AWS.

## Features

- Upload image via REST API
- Resize to predefined dimensions (e.g., thumbnail, medium, large)
- Compress and optimize using Pillow
- Store optimized image in AWS S3
- Event-driven processing via AWS Lambda
- Logs and metrics via CloudWatch

## Tech Stack

- **Python** (FastAPI, Pillow, boto3)
- **AWS Lambda** (image processing)
- **AWS S3** (image storage)
- **AWS API Gateway** (REST endpoint)
- **AWS CloudWatch** (logging/monitoring)

## Architecture Overview

1. Client uploads image via API Gateway.
2. FastAPI handles the request and stores the original image in S3.
3. Lambda is triggered to resize and compress the image.
4. Optimized image is saved back to S3 under a different key.
5. Logs and metrics are captured in CloudWatch.

## Setup

### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/image-resizer-api.git
cd image-resizer-api
```

### 2. Install Dependencies

```bash
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Environment Variables

Copy `.env.example` to `.env` and configure:
```
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
S3_BUCKET_NAME=your-bucket
RESIZE_SIZES=thumbnail:150x150,medium:500x500,large:1024x768
```

### 4. Run Locally

```bash
uvicorn src.main:app --reload
```

### 5. Deploy to AWS

Using AWS SAM
```bash
sam build
sam deploy --guided
```

## API Usage

Request:
`POST /upload`
Upload an image to be resized.
Body: `multipart/form-data`
| Field    | Type    | Description                |
| -------- | ------- | -------------------------- |
| file     | File    | Image file (PNG, JPG, etc.)|

Response:
```json
{
  "original_url": "https://s3.amazonaws.com/bucket/original.jpg",
  "resized_urls": {
    "thumbnail": "https://s3.amazonaws.com/bucket/thumbnail.jpg",
    "medium": "https://s3.amazonaws.com/bucket/medium.jpg",
    "large": "https://s3.amazonaws.com/bucket/large.jpg"
  }
}
```

## Testing

```bash
pytest tests/
```

## Future Improvements

- Add user authentication
- Support WebP and AVIF formats
- Add a web interface for uploads
- Implement image expiration / cleanup policy