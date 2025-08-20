import uuid
from app.database import notifications_collection
from app.utils import utcnow


async def push_notification(payload: dict):
    payload = {
    "notification_id": str(uuid.uuid4()),
    "date_creation": utcnow(),
    "lu": False,
    **payload,
    }
    await notifications_collection.insert_one(payload)
    return payload