from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from jose import JWTError, jwt
from datetime import datetime, timedelta
from .gRPCHandler import getAccountById
from .models import TokenData
import bcrypt

SECRET_KEY = "your_secret_key"  # Replace with a strong secret key
ALGORITHM = "HS256"
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="token")

def verifyPassword(plainPassword: str, hashedPassword: str) -> bool:
    return bcrypt.checkpw(plainPassword.encode('utf-8'), hashedPassword.encode('utf-8'))

def createAccessToken(data: dict, expireDelta: timedelta = None):
    toEncode = data.copy()
    if expireDelta:
        expire = datetime.utcnow() + expireDelta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    toEncode.update({"exp": expire})
    encodedJwt = jwt.encode(toEncode, SECRET_KEY, algorithm=ALGORITHM)
    return encodedJwt

async def getCurrentUser(token: str = Depends(OAUTH2_SCHEME)):
    credentialsException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        userId: str = payload.get("sub")
        if userId is None:
            raise credentialsException
        tokenData = TokenData(userId=userId)
    except JWTError:
        raise credentialsException
    user = await getAccountById(tokenData.userId)
    if user is None:
        raise credentialsException
    return user