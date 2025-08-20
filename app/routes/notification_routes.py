from fastapi import APIRouter

router = APIRouter()

@router.post("/")
def send_notification(user_id: str, message: str):
    return {"to": user_id, "message": message, "status": "sent"}
