from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from .schemas import ExposureEvent 
from .models import ExposureEventDB, UserCriticalityScore
import json
from datetime import datetime
from collections import defaultdict

#todo: move to other place
def _calculate_new_score(old_score: int, severity: str, source: str) -> int:
    """Calculates a new user criticality score."""
    source = source.lower() if source else ""
    severity = severity.lower() if severity else ""

    if source == "malware":
        return 10
    
    if severity == 'high':
        return min(10, old_score + 3)
    elif severity == 'low':
        return min(10, old_score + 1)
    else:
        return old_score


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

#this ensures that tables under Base are created when the application starts
@app.on_event("startup")
def on_startup():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        data_count = db.query(ExposureEventDB).count()
        if data_count == 0:
            print("No events found, loading initial info..")
            
            try:
                with open("/exposure-app/app/alerts.json", "r") as f:
                    data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(f"Error reading alerts.json: {e}")
                return

            user_scores = defaultdict(int)
            times_reported = defaultdict(int)

            for alert in data["alerts"]:
                email = alert["email"]
                source_info = alert["source_info"]
                source = source_info.get("source")

                if source == "malware":
                    user_scores[email] = 10
                else:
                    severity = source_info.get("severity")
                    if severity == "high":
                        user_scores[email] += 3
                    else:
                        user_scores[email] += 1

                times_reported[alert["email"]] +=1

                new_event = ExposureEventDB(
                    id=alert["id"],
                    email=email,
                    source=alert["source_info"]["source"],
                    severity=alert["source_info"].get("severity", "high"),
                    detected_at=datetime.fromisoformat(alert["detected_at"].replace("Z", "+00:00")),
                    created_at=datetime.fromisoformat(alert["created_at"].replace("Z", "+00:00")),
                )
                db.add(new_event)

            for email, score in user_scores.items():
                new_event = UserCriticalityScore(
                    email = email,
                    score = min(score,10) ,
                    times_reported = times_reported[email]
                )
                db.add(new_event)

            db.commit()
            print(f"Successfully loaded {len(data['alerts'])} records.")
        else:
            print("Db already loaded, skipping")


@app.get("/")
async def read_root():
    return {"message": "Hello, World! Your API is up and running."}




@app.post("/exposures", status_code=201)
async def create_exposure_event(exposure: ExposureEvent, db: Session = Depends(get_db)):
    """
    An endpoint to load new exposed credentials and save event to the database.
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


    user_score_record = db.query(UserCriticalityScore).filter(UserCriticalityScore.email == exposure.email).first()

    if user_score_record:
        new_score = _calculate_new_score(
            old_score=user_score_record.score,
            severity=exposure.source_info.severity,
            source=exposure.source_info.source
        )
        user_score_record.score = new_score
        user_score_record.times_reported += 1
    else:
        initial_score = _calculate_new_score(
            old_score=0, 
            severity=exposure.source_info.severity,
            source=exposure.source_info.source
        )
        user_score_record = UserCriticalityScore(
            email=exposure.email,
            score=initial_score,
            times_reported=1
        )
        db.add(user_score_record)

    db.commit()
    
    db.refresh(db_event)
    db.refresh(user_score_record)
    
    return {"message": "Leak event loaded successfully", "event_id": db_event.id}
