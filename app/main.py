from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import products, orders, auth
from fastapi.responses import HTMLResponse
import os
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles


app = FastAPI(title="Neptis Webshop API")

load_dotenv()
origins = os.getenv("CORS_ALLOW_ORIGINS", "*").split(",")

app.mount("/uploads", StaticFiles(directory="storage/uploads"), name="uploads")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router)
app.include_router(orders.router)
app.include_router(auth.router)

@app.get("/")
def root():
    html = "<h2>The Neptis Webshop API is working as expected.</h2><p>For documentation on the API visit <a href='/docs'>this link</a></p>"
    return HTMLResponse(content=html, status_code=200) 
