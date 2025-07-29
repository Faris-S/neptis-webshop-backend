import os
import json

STORAGE_DIR = "storage"

from datetime import datetime

def serialize(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, list):
        return [serialize(o) for o in obj]
    elif isinstance(obj, dict):
        return {k: serialize(v) for k, v in obj.items()}
    return obj


def get_file_path(filename: str) -> str:
    os.makedirs(STORAGE_DIR, exist_ok=True)
    return os.path.join(STORAGE_DIR, filename)

def load_data(filename: str):
    path = get_file_path(filename)
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump([], f)
        return []
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_data(filename: str, data):
    path = get_file_path(filename)
    os.makedirs(STORAGE_DIR, exist_ok=True)
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump([], f)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(serialize(data), f, indent=2, ensure_ascii=False)
