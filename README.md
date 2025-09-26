# Exposure Api
This project is a security-focused API designed to ingest and analyze data exposure incidents. It offers two core functionalities: an endpoint to save the details of new credential leaks, and a system to calculate a cumulative criticality score for each user. This allows teams to proactively monitor and prioritize users based on their evolving risk profile.

### Pull the project
	You know.. just clone the thing

### Build docker image (inside the projec):
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

### About the bonus
For a bonus, an idea was to integrate the 'Have I Been Pwned?' API. This would have allowed us to check a user's entire public breach history the first time we see them. Instead of their risk score starting from zero, it would immediately reflect their past exposures, giving the security team a much more accurate risk assessment from day one.