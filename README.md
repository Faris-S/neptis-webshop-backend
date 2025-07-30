# Neptis Webshop Backend

This repository contains a simple FastAPI backend for a demo webshop. It exposes a REST API for managing products, processing orders and authenticating an admin user. Data is stored in JSON files within the `storage/` folder.

## Project Layout

```
.
├── Dockerfile          - container recipe for running the API
├── requirements.txt    - Python dependencies
├── app/                - FastAPI application package
│   ├── main.py         - application entry point
│   ├── database.py     - JSON file utility
│   ├── models.py       - pydantic models
│   └── routes/         - API route handlers
└── .env.sample         - example environment configuration
```

## Getting Started

### Prerequisites

- Python 3.12.10+
- `pip` for installing dependencies

### Installation

1. Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. (Optional) create a `.env` file based on `.env.sample` to configure CORS:

```bash
cp .env.sample .env
# edit .env if needed
```

### Running the API

Run the application with Uvicorn:

```bash
uvicorn app.main:app --reload
```

By default the server starts on <http://localhost:8000>. API documentation is available at <http://localhost:8000/docs> when running locally.

### Using Docker

You can also build and run the API using Docker:

```bash
docker build -t neptis-webshop-backend .
docker run -p 8000:8000 neptis-webshop-backend
```

## API Overview

Below is a brief summary of the main endpoints. Refer to the interactive docs (`/docs`) for full details.

### Authentication

- `POST /auth/login` – Simulated login route with hardcoded credentials and fake jwt.

### Products

- `GET /products/` – List all products.
- `GET /products/{id}` – Retrieve a single product.
- `POST /products/` – Create a product (requires bearer token).
- `PUT /products/{id}` – Update a product (requires bearer token).
- `DELETE /products/{id}` – Delete a product (requires bearer token).

### Orders

- `GET /orders/` – List all orders (requires bearer token).
- `POST /orders/` – Create a new order.
- `PUT /orders/{id}` – Update order status (requires bearer token).

## Storage

All persistent data lives in the `storage/` directory. When the API runs for the first time it will create:

- `storage/products.json` – product catalogue
- `storage/orders.json` – order records
- `storage/uploads/` – uploaded product images

Note: Docker implementation is not currently set up with volumes, so upon container deletion, the data is lost. This is done as a temporary thing and would be improved upon when doing it with a database.