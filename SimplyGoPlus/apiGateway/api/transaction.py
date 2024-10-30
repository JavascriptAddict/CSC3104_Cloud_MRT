from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ..gRPCHandler import getTransaction, createTransaction, updateTransaction
from ...generated import transaction_pb2, transaction_pb2_grpc
from google.protobuf.json_format import MessageToJson, MessageToDict
import grpc
from ..models import Transaction, AccountResponse
from ..auth import getCurrentUser

transaction = APIRouter()

@transaction.get("/transactions/{transactionId}")
async def get_transaction(transactionId: str, currentUser: AccountResponse = Depends(getCurrentUser)):
    transaction = await getTransaction(transactionId)
    if transaction is None or transaction.transactionId == "":
        return {"status": 404, "message": "Transaction ID not found"}
    return {"message": "Transaction retrieved", "data": MessageToDict(transaction)}

@transaction.post("/transactions/create")
async def create_transaction(transaction: Transaction, currentUser: AccountResponse = Depends(getCurrentUser)):
    newTransaction = await createTransaction(transaction)
    if newTransaction is None or newTransaction.transactionId == "":
        return {"status": 500, "message": "Error occurred"}
    return {"message": "Transaction created", "data": MessageToDict(newTransaction)}

@transaction.put("/transactions/update/{transactionId}")
async def update_transaction(transactionId: str, transaction: Transaction, currentUser: AccountResponse = Depends(getCurrentUser)):
    updatedTransaction = await updateTransaction(transactionId, transaction)
    if updatedTransaction is None:
        return {"status": 500, "message": "Error occurred"}
    return  {"message": "Transaction updated", "data": MessageToDict(updatedTransaction)}
