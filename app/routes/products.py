from fastapi import APIRouter, HTTPException
from models import Product
from database import load_data, save_data
from datetime import datetime
from fastapi import Depends
from routes.auth import verify_token

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/")
def get_all_products():
    return load_data("products.json")

@router.get("/{product_id}")
def get_product(product_id: int):
    products = load_data("products.json")
    for product in products:
        if product["id"] == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")


@router.post("/", dependencies=[Depends(verify_token)])
def create_product(product: Product):
    products = load_data("products.json")
    product.created_at = datetime.now()
    products.append(product.dict())
    save_data("products.json", products)
    return {"message": "Product added successfully"}

@router.put("/{product_id}", dependencies=[Depends(verify_token)])
def update_product(product_id: int, updated_product: Product):
    products = load_data("products.json")
    for idx, product in enumerate(products):
        if product["id"] == product_id:
            updated_product.created_at = product["created_at"]
            products[idx] = updated_product.dict()
            save_data("products.json", products)
            return {"message": "Product updated successfully"}
    raise HTTPException(status_code=404, detail="Product not found")

@router.delete("/{product_id}", dependencies=[Depends(verify_token)])
def delete_product(product_id: int):
    products = load_data("products.json")
    products = [p for p in products if p["id"] != product_id]
    save_data("products.json", products)
    return {"message": "Product deleted successfully"}
