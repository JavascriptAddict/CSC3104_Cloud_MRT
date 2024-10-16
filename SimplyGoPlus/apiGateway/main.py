from fastapi import FastAPI
from .api.account import account

app = FastAPI()

# Declare the services IP destination. Change when needed in deployment
TRANSACTION_SERVICE_ADDRESS = "localhost:50052"
TRIP_SERVICE_ADDRESS = "localhost:50053"
VISION_SERVICE_ADDRESS = "localhost:50054"
    
@app.get("/")
async def root():
    return {"message": "Welcome to SimplyGoPlus"}

app.include_router(account)
