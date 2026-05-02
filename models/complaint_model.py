from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ComplaintCreate(BaseModel):
    title: str
    description: str
    department: str 
    location: str          # ← ADD THIS LINE
    priority: str         

class ComplaintStatusUpdate(BaseModel):
    status: str            

class ComplaintResponse(BaseModel):
    id: str
    title: str
    description: str
    department: str
    priority: str
    status: str
    filed_by: Optional[str] = None
    created_at: Optional[datetime] = None

class ComplaintSummary(BaseModel):
    total: int
    open: int
    resolved: int