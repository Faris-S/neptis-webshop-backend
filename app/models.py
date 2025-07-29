from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    quantity: int
    image_url: str
    created_at: datetime

class OrderItem(BaseModel):
    product_id: int
    quantity: int

class CustomerInfo(BaseModel):
    first_name: str
    last_name: str
    address: str
    phone: str
    email: Optional[EmailStr] = None

class Order(BaseModel):
    id: int
    items: List[OrderItem]
    created_at: datetime
    status: str
    status_date: Optional[datetime] = None
    customer: CustomerInfo

class AdminUser(BaseModel):
    username: str
    password: str
