from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import requests
import os
from auth import oauth2_scheme

router = APIRouter()

N8N_WEBHOOK_URL = os.environ.get("N8N_WEBHOOK_URL")
SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
ALGORITHM = "HS256"

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return username

@router.post("")
async def upload_resume(file: UploadFile = File(...), current_user: str = Depends(get_current_user)):
    if not N8N_WEBHOOK_URL:
        raise HTTPException(status_code=500, detail="N8N_WEBHOOK_URL not configured")

    try:
        files = {"file": (file.filename, await file.read(), file.content_type)}
        response = requests.post(N8N_WEBHOOK_URL, files=files)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to send file to n8n: {e}")
    
    return {"message": "File successfully uploaded and sent to n8n"}