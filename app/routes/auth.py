from fastapi import APIRouter, HTTPException
from jose import jwt
from app.config import SECRET_KEY, ALGORITHM
from app.database import get_user_by_username

router = APIRouter()

@router.post("/login")
async def login(username: str, password: str):
    user = await get_user_by_username(username)
    if not user or not user.verify_password(password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token_data = {"sub": user.username}
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": token, "token_type": "bearer"}
