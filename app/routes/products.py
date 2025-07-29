from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
from models import Product
from database import load_data, save_data
from datetime import datetime
from routes.auth import verify_token
import os
import uuid
import shutil

router = APIRouter(prefix="/products", tags=["Products"])

UPLOAD_DIR = "storage/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

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
async def create_product(
    id: int = Form("id"),
    name: str = Form("name"),
    description: str = Form("description"),
    price: float = Form("price"),
    image: UploadFile = File("image")
):
    products = load_data("products.json")

    file_ext = os.path.splitext(image.filename)[1]
    image_filename = f"{uuid.uuid4().hex}{file_ext}"
    image_path = os.path.join(UPLOAD_DIR, image_filename)

    with open(image_path, "wb") as f:
        shutil.copyfileobj(image.file, f)

    new_product = {
        "id": id,
        "name": name,
        "description": description,
        "price": price,
        "image_url": image_filename,
        "created_at": datetime.now().isoformat()
    }
    print(products)
    print(f"Adding new product: {new_product}")
    products.append(new_product)
    save_data("products.json", products)
    return {"message": "Product added successfully", "product": new_product}

@router.put("/{product_id}", dependencies=[Depends(verify_token)])
async def update_product(
    product_id: int,
    name: str = Form("name"),
    description: str = Form("description"),
    price: float = Form("price"),
    image: UploadFile = File("image")
):
    products = load_data("products.json")

    for idx, product in enumerate(products):
        if product["id"] == product_id:
            old_image_url = product.get("image_url")
            if old_image_url:
                old_image_path = os.path.join(".", old_image_url.lstrip("/"))
                if os.path.exists(old_image_path):
                    try:
                        os.remove(old_image_path)
                    except Exception as e:
                        print(f"Failed to delete old image: {e}")

            file_ext = os.path.splitext(image.filename)[1]
            image_filename = f"{uuid.uuid4().hex}{file_ext}"
            image_path = os.path.join(UPLOAD_DIR, image_filename)

            with open(image_path, "wb") as f:
                shutil.copyfileobj(image.file, f)

            updated_product = {
                "id": product_id,
                "name": name,
                "description": description,
                "price": price,
                "image_url": image_filename,
                "created_at": product["created_at"]
            }

            products[idx] = updated_product
            save_data("products.json", products)

            return {"message": "Product updated successfully", "product": updated_product}

    raise HTTPException(status_code=404, detail="Product not found")

@router.delete("/{product_id}", dependencies=[Depends(verify_token)])
def delete_product(product_id: int):
    products = load_data("products.json")
    product_to_delete = next((p for p in products if p["id"] == product_id), None)

    if not product_to_delete:
        raise HTTPException(status_code=404, detail="Product not found")

    image_path = UPLOAD_DIR + product_to_delete.get("image_url")
    if image_path and os.path.exists(image_path):
        try:
            os.remove(image_path)
        except Exception as e:
            print(f"Failed to delete image: {e}")

    products = [p for p in products if p["id"] != product_id]
    save_data("products.json", products)

    return {"message": "Product deleted successfully"}

