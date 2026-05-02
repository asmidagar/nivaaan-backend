# routes/vendor_routes.py

from fastapi import APIRouter, HTTPException
from database import vendors_collection
from models.vendor_model import VendorCreate
from bson import ObjectId

router = APIRouter()


# -----------------------------------------------
# GET /api/vendors
# Returns all vendors
# -----------------------------------------------
@router.get("/")
async def get_vendors():
    try:
        vendors = []
        for vendor in vendors_collection.find():
            vendors.append({
                "id": str(vendor["_id"]),
                "name": vendor.get("name", ""),
                "department": vendor.get("department", ""),
                "complaints": vendor.get("complaints", 0)
            })
        return vendors
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------------------------
# POST /api/vendors
# Adds a new vendor
# -----------------------------------------------
@router.post("/", status_code=201)
async def add_vendor(vendor: VendorCreate):
    try:
        new_vendor = {
            "name": vendor.name,
            "department": vendor.department,
            "complaints": 0
        }
        result = vendors_collection.insert_one(new_vendor)
        return {
            "message": "Vendor added successfully!",
            "id": str(result.inserted_id)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------------------------
# DELETE /api/vendors/{id}
# Deletes a vendor
# -----------------------------------------------
@router.delete("/{vendor_id}")
async def delete_vendor(vendor_id: str):
    try:
        result = vendors_collection.delete_one(
            {"_id": ObjectId(vendor_id)}
        )
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=404,
                detail="Vendor not found"
            )
        return {"message": "Vendor deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))