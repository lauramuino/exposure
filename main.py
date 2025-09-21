from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional
from datetime import datetime

app = FastAPI(
    title="Exposure API",
    description="User scoring service for exposed credentals.",
    version="1.0.1"
)

class SourceInfo(BaseModel):
	source: str
	severity: Optional[str]

class ExposureEvent(BaseModel):
	id: UUID
	email: EmailStr
	source_info: SourceInfo
	detected_at: datetime
	created_at: datetime

@app.get("/")
async def read_root():
    """
    Root endpoint that returns a welcome message.
    """
    return {"message": "Hello, World! Your API is up and running."}

@app.post("/exposures")
async def create_exposure_event(exposure: ExposureEvent):
    """
    An endpoint to load new exposed credentials.
    """
    print(f"email: {exposure.email}")
    return {"message": "Leak event loaded successfully"}

# To run this app, you would use an ASGI server like Uvicorn:
# uvicorn main:app --host 0.0.0.0 --port 8000 --reload
