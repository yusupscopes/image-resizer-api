# Development Plan – Image Resizer & Optimizer API

## Goal

Build a scalable, serverless image processing API that automatically resizes and compresses user-uploaded images using AWS services and Python.

---

## Phases

### Phase 1 – MVP (Minimum Viable Product)
- [x] Define project scope and use cases
- [x] Setup FastAPI app for image upload
- [x] Upload original image to S3
- [x] Trigger AWS Lambda to process image
- [x] Resize and optimize image using Pillow
- [x] Save resized versions back to S3
- [x] Return S3 URLs to the client

### Phase 2 – Infrastructure as Code (IaC)
- [x] Use AWS SAM to define and deploy API Gateway, Lambda, and S3
- [x] Configure permissions and roles (IAM)
- [x] Setup environment variables using AWS Parameter Store or SAM config

### Phase 3 – Monitoring & Logging
- [x] Integrate AWS CloudWatch logs
- [x] Add custom CloudWatch metrics for monitoring
- [x] Add request/response logging

### Phase 4 – Testing & Automation
- [ ] Write unit tests for image processing logic
- [ ] Write integration tests for API endpoints
- [ ] Set up CI workflow (GitHub Actions or CodePipeline)

### Phase 5 – Enhancements
- [ ] Add AVIF/WebP format support
- [ ] Allow custom dimensions in query
- [ ] Add signed URLs for private access
- [ ] Build optional web UI for upload preview

---

## Folder Structure

See [`README.md`](./README.md) for the detailed folder structure.

---

## TODO

- [ ] Create a sample image set for testing
- [ ] Measure image size reduction metrics
- [ ] Benchmark Lambda cold starts and performance
- [ ] Deploy and test in a real AWS environment
