from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ..gRPCHandler import getTransaction
from google.protobuf.json_format import MessageToJson, MessageToDict
import grpc
from ..models import AccountResponse
from ..auth import getCurrentUser

transaction = APIRouter()

@transaction.get("/transactions")
async def get_transaction(currentUser: AccountResponse = Depends(getCurrentUser)):
    transactions = MessageToDict(await getTransaction(currentUser.userId))
    return {"message": "Transactions retrieved", "data": transactions}
