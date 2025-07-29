from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from models import AdminUser
from fastapi import Depends, HTTPException, status, Header
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix="/auth", tags=["Auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

#Hardcoded for demo
FAKE_ADMIN_USER = {
    "username": "admin",
    "password": "admin123"
}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if (
        form_data.username == FAKE_ADMIN_USER["username"] and
        form_data.password == FAKE_ADMIN_USER["password"]
    ):
        return {
            "access_token": "fake-jwt-token",
            "token_type": "bearer"
        }
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

def verify_token(token: str = Depends(oauth2_scheme)):
    if token != "fake-jwt-token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )