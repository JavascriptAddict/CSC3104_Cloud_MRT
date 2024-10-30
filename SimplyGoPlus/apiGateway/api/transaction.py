from fastapi import APIRouter
from pydantic import BaseModel

from ..gRPCHandler import getTransaction, createTransaction, updateTransaction
from ...generated import transaction_pb2, transaction_pb2_grpc
from google.protobuf.json_format import MessageToJson, MessageToDict
import grpc
from ..models import Transaction


transaction = APIRouter()

@transaction.get("/transactions/{transactionId}")
async def get_transaction(transactionId: str):
    transaction = await getTransaction(transactionId)
    if transaction is None or transaction.transactionId == "":
        return {"status": 404, "message": "Transaction ID not found"}
    return {"message": "Transaction retrieved", "data": MessageToDict(transaction)}

@transaction.post("/transactions/create")
async def create_transaction(transaction: Transaction):
    newTransaction = await createTransaction(transaction)
    if newTransaction is None or newTransaction.transactionId == "":
        return {"status": 500, "message": "Error occured"}
    return {"message": "Transaction created", "data": MessageToDict(newTransaction)}

@transaction.put("/transactions/update/{transactionId}")
async def update_transaction(transactionId: str, transaction: Transaction):
    updatedTransaction = await updateTransaction(transactionId, transaction)
    if updatedTransaction is None:
        return {"status": 500, "message": "Error occured"}
    return  {"message": "Transaction updated", "data": MessageToDict(updatedTransaction)}
