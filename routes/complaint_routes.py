# routes/complaint_routes.py

from fastapi import APIRouter, HTTPException, Header
from typing import Optional
from datetime import datetime
from bson import ObjectId
from database import complaints_collection
from models.complaint_model import ComplaintCreate, ComplaintStatusUpdate
from utils.jwt_handler import verify_token

router = APIRouter()


# -----------------------------------------------
# 📌 GET /api/complaints
# Called by: ComplaintList.js
# Expects:  nothing
# Returns:  [ { title, description, department, status, ... } ]
# -----------------------------------------------
@router.get("/")
async def get_all_complaints():

    try:

        complaints = []

        for complaint in complaints_collection.find():
            complaints.append({
                "id": str(complaint["_id"]),
                "title": complaint.get("title", ""),
                "description": complaint.get("description", ""),
                "department": complaint.get("department", ""),
                "priority": complaint.get("priority", ""),
                "status": complaint.get("status", "Open"),
                "filed_by": str(complaint.get("filed_by", "")),
                "created_at": complaint.get("created_at", None)
            })

        return complaints   # ✅ returns array — matches ComplaintList.js check

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------------------------
# 📌 POST /api/complaints
# Called by: CreateComplaint.js
# Expects:  { title, description, department, priority }
# Returns:  { message, id }
# -----------------------------------------------
@router.post("/", status_code=201)
async def create_complaint(
    complaint: ComplaintCreate,
    authorization: Optional[str] = Header(None)
):

    try:

        # 1. Extract user from token if available
        filed_by = None
        if authorization and authorization.startswith("Bearer "):
            token = authorization.split(" ")[1]
            payload = verify_token(token)
            if payload:
                filed_by = payload.get("id")

        # 2. Build complaint document
        new_complaint = {
            "title": complaint.title,
            "description": complaint.description,
            "department": complaint.department,
            "location": complaint.location,      # ← add this line
            "priority": complaint.priority,
            "status": "Open",
            "filed_by": filed_by,
            "created_at": datetime.utcnow()
        }

        # 3. Insert into MongoDB
        result = complaints_collection.insert_one(new_complaint)

        return {
            "message": "Complaint created successfully!",
            "id": str(result.inserted_id)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------------------------
# 📌 GET /api/complaints/summary/status
# Called by: Dashboard.js
# Expects:  JWT token in header
# Returns:  { total, open, resolved }
# -----------------------------------------------
@router.get("/summary/status")
async def get_summary(
    authorization: Optional[str] = Header(None)
):

    try:

        # Count complaints by status
        total = complaints_collection.count_documents({})
        open_count = complaints_collection.count_documents(
            {"status": "Open"}
        )
        resolved_count = complaints_collection.count_documents(
            {"status": "Resolved"}
        )

        # ✅ Matches exactly what Dashboard.js expects:
        # { total, open, resolved }
        return {
            "total": total,
            "open": open_count,
            "resolved": resolved_count
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------------------------
# 📌 GET /api/complaints/{id}
# Get single complaint by ID
# -----------------------------------------------
@router.get("/{complaint_id}")
async def get_complaint(complaint_id: str):

    try:

        complaint = complaints_collection.find_one(
            {"_id": ObjectId(complaint_id)}
        )

        if not complaint:
            raise HTTPException(
                status_code=404,
                detail="Complaint not found"
            )

        return {
            "id": str(complaint["_id"]),
            "title": complaint.get("title", ""),
            "description": complaint.get("description", ""),
            "department": complaint.get("department", ""),
            "priority": complaint.get("priority", ""),
            "status": complaint.get("status", "Open"),
            "filed_by": str(complaint.get("filed_by", "")),
            "created_at": complaint.get("created_at", None)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------------------------
# 📌 PATCH /api/complaints/{id}/status
# Called by: UpdateStatus.js
# Expects:  { status: "Open/In Progress/Resolved" }
# Returns:  { message }
# -----------------------------------------------
@router.patch("/{complaint_id}/status")
async def update_status(
    complaint_id: str,
    status_update: ComplaintStatusUpdate
):

    try:

        # 1. Validate status value
        valid_statuses = ["Open", "In Progress", "Resolved"]
        if status_update.status not in valid_statuses:
            raise HTTPException(
                status_code=400,
                detail=f"Status must be one of: {valid_statuses}"
            )

        # 2. Update in MongoDB
        result = complaints_collection.update_one(
            {"_id": ObjectId(complaint_id)},
            {
                "$set": {
                    "status": status_update.status,
                    "updated_at": datetime.utcnow()
                }
            }
        )

        # 3. Check if complaint existed
        if result.matched_count == 0:
            raise HTTPException(
                status_code=404,
                detail="Complaint not found"
            )

        return {"message": f"Status updated to '{status_update.status}'"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------------------------
# 📌 DELETE /api/complaints/{id}
# Delete a complaint by ID
# -----------------------------------------------
@router.delete("/{complaint_id}")
async def delete_complaint(complaint_id: str):

    try:

        result = complaints_collection.delete_one(
            {"_id": ObjectId(complaint_id)}
        )

        if result.deleted_count == 0:
            raise HTTPException(
                status_code=404,
                detail="Complaint not found"
            )

        return {"message": "Complaint deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

