import io
from PIL import Image
import pytest
from src.resize import resize_and_upload

class MockS3Client:
    def __init__(self):
        self.uploads = []

    def put_object(self, Bucket, Key, Body, ContentType):
        self.uploads.append((Key, ContentType))
        assert ContentType == "image/jpeg"

@pytest.fixture
def dummy_image_bytes():
    img = Image.new("RGB", (800, 600), color="blue")
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG")
    buffer.seek(0)
    return buffer.read()

def test_resize_and_upload(monkeypatch, dummy_image_bytes):
    mock_s3 = MockS3Client()
    monkeypatch.setattr("src.resize.s3", mock_s3)

    resize_and_upload(dummy_image_bytes, "uploads/test.jpg")

    # Expect 3 resized variants
    assert len(mock_s3.uploads) == 3
    for key, _ in mock_s3.uploads:
        assert key.startswith("resized/")
        assert key.endswith("test.jpg")
