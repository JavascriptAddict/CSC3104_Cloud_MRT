
from fastapi import APIRouter, Depends, UploadFile
from ..models import Account, AccountCreation, AccountResponse
from ..auth import getCurrentUser
from google.protobuf.json_format import MessageToDict
from ..gRPCHandler import getAccountById, getUserByImage
import json

gantry = APIRouter()

@gantry.post("/gantry/starttrip")
async def start_trip(image: UploadFile):
    fileBytes = await image.read()
    account = await getUserByImage(fileBytes)
    account = await getAccountById(account.userId)
    return {"message": "Account retrieved", "data": MessageToDict(account)}

