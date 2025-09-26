from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional
from datetime import datetime

class SourceInfo(BaseModel):
	source: str
	severity: Optional[str] = None

class ExposureEvent(BaseModel):
	id: UUID
	email: EmailStr
	source_info: SourceInfo
	detected_at: datetime
	created_at: datetime

#pydantic validation models (for requests)