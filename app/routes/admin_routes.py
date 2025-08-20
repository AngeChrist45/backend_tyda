from fastapi import APIRouter, Depends, HTTPException
from services.auth import decode_access_token

router = APIRouter()

@router.get("/dashboard")
def get_admin_dashboard(token: str = Depends()):
    payload = decode_access_token(token)
    if not payload or payload.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Access forbidden")
    return {"message": "Welcome to the Admin Dashboard"}
