from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from .auth import createAccessToken, verifyPassword
from .gRPCHandler import getAccountByUsername
from .api.account import account
from .api.transaction import transaction
from .models import Token
from datetime import timedelta

TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

# Declare the services IP destination. Change when needed in deployment
TRANSACTION_SERVICE_ADDRESS = "localhost:50052"
TRIP_SERVICE_ADDRESS = "localhost:50053"
VISION_SERVICE_ADDRESS = "localhost:50054"
    
@app.get("/")
async def root():
    return {"message": "Welcome to SimplyGoPlus"}

@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await getAccountByUsername(form_data.username)
    if not user or not verifyPassword(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    accessTokenExpiry = timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    accessToken = createAccessToken(data={"sub": user.userId}, expireDelta=accessTokenExpiry)
    return {"access_token": accessToken, "token_type": "bearer"}

app.include_router(account)
app.include_router(transaction)
