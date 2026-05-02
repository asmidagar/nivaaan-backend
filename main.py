# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.auth_routes import router as auth_router
from routes.complaint_routes import router as complaint_router
from routes.vendor_routes import router as vendor_router

import sys
print(f"Python version: {sys.version}")
print("Starting NIVAAAN API...")

# -----------------------------------------------
# 🚀 App Initialization
# -----------------------------------------------
app = FastAPI(
    title="NIVAAAN API",
    description="Complaint Management System Backend",
    version="1.0.0"
)


# -----------------------------------------------
# 🌐 CORS Middleware
# Allows React frontend to talk to FastAPI backend
# -----------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",   # React default port
        "http://localhost:5173",   # Vite default port ✅ your frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],           # GET, POST, PATCH, DELETE etc
    allow_headers=["*"],           # Authorization, Content-Type etc
)


# -----------------------------------------------
# 📌 Routers
# -----------------------------------------------
app.include_router(
    auth_router,
    prefix="/api/auth",            # → /api/auth/login
    tags=["Auth"]                  #   /api/auth/register
)

app.include_router(
    complaint_router,
    prefix="/api/complaints",      # → /api/complaints
    tags=["Complaints"]            #   /api/complaints/summary/status
)                                  #   /api/complaints/{id}/status


# -----------------------------------------------
# ✅ Health Check
# -----------------------------------------------
@app.get("/")
def root():
    return {
        "message": "NIVAAAN API is running! 🚀",
        "docs": "http://localhost:5000/docs"
    }

# main.py — add these two lines


app.include_router(
    vendor_router,
    prefix="/api/vendors",
    tags=["Vendors"]
)
