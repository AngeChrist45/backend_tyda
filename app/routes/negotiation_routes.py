from fastapi import APIRouter

router = APIRouter()

@router.post("/")
def start_negotiation(order_id: str, vendor_id: str):
    return {"message": f"Negotiation started for order {order_id} with vendor {vendor_id}"}

@router.get("/{negotiation_id}")
def get_negotiation(negotiation_id: str):
    return {"negotiation_id": negotiation_id, "status": "pending"}
