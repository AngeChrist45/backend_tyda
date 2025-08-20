from fastapi import APIRouter

router = APIRouter()

@router.post("/")
def create_order(product_id: str, quantity: int):
    return {"order_id": "order123", "product_id": product_id, "quantity": quantity, "status": "created"}

@router.get("/{order_id}")
def get_order(order_id: str):
    return {"order_id": order_id, "status": "in progress"}
