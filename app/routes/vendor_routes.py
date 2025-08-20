from fastapi import APIRouter

router = APIRouter()

@router.post("/")
def register_vendor(name: str, email: str):
    return {"vendor_id": "vnd123", "name": name, "email": email, "status": "registered"}

@router.get("/{vendor_id}")
def get_vendor(vendor_id: str):
    return {"vendor_id": vendor_id, "name": "Example Vendor", "status": "active"}
