import io
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_upload_image_success(monkeypatch):
    # Mock S3 client
    class MockS3Client:
        def put_object(self, Bucket, Key, Body, ContentType):
            assert Bucket
            assert Key.endswith(".jpg")
            assert Body
            assert ContentType == "image/jpeg"

    monkeypatch.setattr("src.main.s3", MockS3Client())

    image_data = io.BytesIO(b"fake image bytes")
    files = {"file": ("test.jpg", image_data, "image/jpeg")}
    response = client.post("/upload", files=files)

    assert response.status_code == 200
    assert "original_key" in response.json()
