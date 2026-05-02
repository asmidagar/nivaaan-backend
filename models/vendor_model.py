# models/vendor_model.py

from pydantic import BaseModel
from typing import Optional


class VendorCreate(BaseModel):
    name: str
    department: str


class VendorResponse(BaseModel):
    id: str
    name: str
    department: str
    complaints: Optional[int] = 0