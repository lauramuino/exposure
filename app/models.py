from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from uuid import uuid4
from .database import Base

class ExposureEventDB(Base):
    __tablename__ = "exposure_events"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    email = Column(String, index=True, nullable=False)
    source = Column(String, nullable=False)
    severity = Column(String, nullable=True)
    detected_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False)

#sql alchemy database model (the info about the event as a single table for now)