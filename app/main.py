from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from .schemas import ExposureEvent 
from .models import ExposureEventDB
import json
from datetime import datetime

# Dependency injection?? to get a DB session
#This is a standard FastAPI pattern to manage database sessions for each API request.
#how does fast api manages lifecycles??
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI(
    title="Exposure API",
    description="User scoring service for exposed credentals",
    version="1.0.1"
)

#this ensures that exposure_events table is created when the application starts
@app.on_event("startup")
def on_startup():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        data_count = db.query(ExposureEventDB).count()
        if data_count == 0:
            print("No events found, loading initial info..")
            
            with open("/exposure-app/app/alerts.json", "r") as f:
                data = json.load(f)

            for alert in data["alerts"]:
                new_event = ExposureEventDB(
                    id=alert["id"],
                    email=alert["email"],
                    source=alert["source_info"]["source"],
                    severity=alert["source_info"].get("severity", "high"),
                    detected_at=datetime.fromisoformat(alert["detected_at"].replace("Z", "+00:00")),
                    created_at=datetime.fromisoformat(alert["created_at"].replace("Z", "+00:00")),
                )
                db.add(new_event)
     
            db.commit()
            print(f"Successfully loaded {len(data['alerts'])} records.")
        else:
            print("Db already loaded, skipping")

    finally:
        db.close()

@app.get("/")
async def read_root():
    return {"message": "Hello, World! Your API is up and running."}

@app.post("/exposures", status_code=201)
async def create_exposure_event(exposure: ExposureEvent, db: Session = Depends(get_db)):
    """
    An endpoint to load new exposed credentials and save them to the database.
    """
    db_event = ExposureEventDB(
        id=exposure.id,
        email=exposure.email,
        source=exposure.source_info.source,
        severity=exposure.source_info.severity,
        detected_at=exposure.detected_at,
        created_at=exposure.created_at
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    
    return {"message": "Leak event loaded successfully", "event_id": db_event.id}
