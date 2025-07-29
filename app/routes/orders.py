from fastapi import APIRouter, HTTPException
from models import Order
from database import load_data, save_data
from datetime import datetime
from fastapi import Depends
from routes.auth import verify_token

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.get("/", dependencies=[Depends(verify_token)])
def get_all_orders():
    return load_data("orders.json")

@router.post("/")
def create_order(order: Order):
    orders = load_data("orders.json")
    order.created_at = datetime.now()
    order.status = "Pending"
    orders.append(order.dict())
    save_data("orders.json", orders)
    return {"message": "Order created and admin notified"}

@router.put("/{order_id}", dependencies=[Depends(verify_token)])
def update_order_status(order_id: int, status: str):
    orders = load_data("orders.json")
    for idx, order in enumerate(orders):
        if order["id"] == order_id:
            orders[idx]["status"] = status
            save_data("orders.json", orders)
            return {"message": "Order status updated"}
    raise HTTPException(status_code=404, detail="Order not found")
