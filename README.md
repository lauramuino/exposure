### Build docker image:
	docker build -t python-api .

### Run docker container:
	docker compose up -d

### Access api endpoints:
	http://localhost:8000/exposures

### Access automatically generated documentation:
	http://localhost:8000/redoc
	http://localhost:8000/docs

### A curl example for new events:

curl -X POST "http://127.0.0.1:8000/exposures" \
-H "Content-Type: application/json" \
-d '{"id": "a458103e-7c3b-4e0d-9b5f-25417d6e4b8f", "email": "javier.gutierrez@gmail.com", "source_info": {"source": "data breach", "severity": "high"}, "detected_at": "2025-09-16T18:50:13.262Z", "created_at": "2025-09-16T18:54:13.262Z"}'

### Other curl examples for consulting:

curl "http://127.0.0.1:8000/criticality-score?javier.gutierrez@gmail.com"
curl "http://127.0.0.1:8000/criticality-score"

