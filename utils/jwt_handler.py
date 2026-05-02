# utils/jwt_handler.py

from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional

# -----------------------------------------------
# 🔐 Configuration
# -----------------------------------------------
SECRET_KEY = "nivaaan_super_secret_key_change_in_production"
ALGORITHM = "HS256"
EXPIRE_MINUTES = 60 * 24   # 24 hours


# -----------------------------------------------
# ✅ CREATE token
# Called by: auth_routes.py → login()
# -----------------------------------------------
def create_token(data: dict) -> str:

    payload = data.copy()

    # Add expiry time to token
    expire = datetime.utcnow() + timedelta(minutes=EXPIRE_MINUTES)
    payload.update({"exp": expire})

    # Generate JWT token
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return token


# -----------------------------------------------
# ✅ VERIFY token
# Called by: complaint_routes.py → create_complaint()
# -----------------------------------------------
def verify_token(token: str) -> Optional[dict]:

    try:

        # Decode and verify token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload

    except JWTError:
        return None   # invalid or expired token


# -----------------------------------------------
# ✅ EXTRACT user from Authorization header
# Helper used in protected routes
# -----------------------------------------------
def get_current_user(authorization: Optional[str]) -> Optional[dict]:

    if not authorization:
        return None

    if not authorization.startswith("Bearer "):
        return None

    try:

        token = authorization.split(" ")[1]
        payload = verify_token(token)
        return payload

    except Exception:
        return None
