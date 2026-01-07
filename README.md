# Image Processing Backend Service

A robust, production-ready FastAPI service designed for mobile app integration. This service handles high-efficiency image uploads, performs deterministic mock skin analysis, and provides structured JSON responses with rich metadata.

## Key Features
Asynchronous I/O: Built with FastAPI for high-concurrency and low-latency performance.

Memory Efficient: Uses shutil streaming for file uploads to handle files up to 5MB without RAM spikes.

Deterministic Mock Analysis: Uses SHA-256 hashing of Image IDs to ensure consistent analysis results for the same image while providing variety across different uploads.

Human-Readable Metadata: Automatically converts raw file bytes into readable KB/MB formats in the response.

Structured Logging: Detailed traceability with timestamps and log levels (INFO, WARNING, ERROR) for security auditing.

Security: API Key authentication enforced via FastAPI Dependency Injection.

Containerized: Fully Dockerized with Docker Compose, featuring volume persistence and hot-reloading for development.

## Tech Stack
Language: Python 3.11

Framework: FastAPI (ASGI)

Validation: Pydantic v2 (Strict typing)

Server: Uvicorn

Containerization: Docker & Docker Compose

## Project Structure
image-processing-service/
├── app/
│   ├── api/v1/         # Route controllers & Endpoint definitions
│   ├── core/           # Security (API Key) & Global Config (Pydantic Settings)
│   ├── schemas/        # Pydantic models (Request/Response validation)
│   ├── services/       # Business logic (File I/O & Mock AI Logic)
│   ├── utils/          # Utilities (Formatting, unit conversion)
│   └── main.py         # App entry point & Logging configuration
├── uploads/            # Local persistent storage for images
├── .dockerignore       # Optimized Docker build exclusions
├── Dockerfile          # Multi-stage build container definition
├── docker-compose.yml  # Service orchestration & Volume mapping
├── requirements.txt    # Project dependencies
└── README.md           # Technical Documentation

## How to Run
1. Using Docker (Recommended)
This ensures environment parity. The setup includes a volume mount to the ./uploads directory to persist data.

Build and Start:
docker compose up --build

Stop the Service:
docker compose down

2. Manual Local Setup
Create a Virtual Environment:
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
Install Dependencies:
pip install -r requirements.txt
Run the Application:
uvicorn app.main:app --reload

## API Documentation & Testing
Once running, access the interactive docs at:

Swagger UI: http://localhost:8000/docs

Redoc: http://localhost:8000/redoc

Authentication
All endpoints (except health check) require a security header:

Header Key: X-API-KEY

Header Value: interview-test-key-123

Step-by-Step Testing via cURL
Step 1: Upload an Image

Bash

curl -X POST "http://localhost:8000/api/v1/upload" \
     -H "X-API-KEY: interview-test-key-123" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@your_photo.jpg"
Note the image_id returned in the response.

Step 2: Analyze the Image

Bash

curl -X POST "http://localhost:8000/api/v1/analyze" \
     -H "X-API-KEY: interview-test-key-123" \
     -H "Content-Type: application/json" \
     -d '{"image_id": "IMAGE_ID_RETURNED_UPLOAD"}'

## Engineering Decisions & Assumptions
Persistence: A Docker volume is used to map the host ./uploads folder to the container. This prevents data loss when the container is rebuilt or restarted.

Deterministic Mock Engine: To simulate real-world AI, we use a numeric seed generated from a SHA-256 hash of the image_id. This ensures that calling the analysis for the same image always yields the same result.

Performance: By using shutil.copyfileobj, we stream the file directly to disk, ensuring the service can handle maximum file sizes (5MB) with minimal memory overhead.

Human Readable Metadata: The service implements a utility to convert raw file bytes into human-friendly strings (e.g., "1.45 MB"), improving the developer experience for frontend teams.

### Production Roadmap
Database Integration: Migrate from filesystem lookups to a database (PostgreSQL) for metadata tracking and user-image ownership.

Object Storage: Transition from local storage to AWS S3 or GCP Buckets to allow for horizontal scaling.

Asynchronous Tasks: Move analysis logic to Celery + Redis background workers to prevent blocking the API event loop during intensive processing.

Real World Image Analysis Integration: Transition to a real world image analysis integration.

Rate Limiting: Implement limits on the /upload endpoint to mitigate DoS risks and storage abuse.