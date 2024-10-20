from fastapi import APIRouter
from pydantic import BaseModel
from ...generated import transaction_pb2, transaction_pb2_grpc
from google.protobuf.json_format import MessageToJson, MessageToDict
import grpc
import json

TRANSACTION_SERVICE_ADDRESS = "localhost:50051"

class Transaction(BaseModel):
    amount: float
    walletId: str

class TransactionCreation(Transaction):
    pass
    
class TransactionResponse(Transaction):
    transactionId: str
    timestamp: str
    
transaction = APIRouter()

async def getTransaction(transactionId) -> None:
    async with grpc.aio.insecure_channel(TRANSACTION_SERVICE_ADDRESS) as channel:
        stub = transaction_pb2_grpc.TransactionStub(channel)
        response = await stub.GetTransaction(transaction_pb2.TransactionRequest(transactionId=transactionId))
    return response

async def createTransaction(transaction) -> None:
    async with grpc.aio.insecure_channel(TRANSACTION_SERVICE_ADDRESS) as channel:
        stub = transaction_pb2_grpc.TransactionStub(channel)
        response = await stub.CreateTransaction(transaction_pb2.CreateTransactionRequest(amount=transaction.amount, walletId=transaction.walletId))
    return response

@transaction.get("/transactions/{transactionId}")
async def get_transaction(transactionId: str):
    transaction = await getTransaction(transactionId)
    if transaction is None or transaction.transactionId == "":
        return {"status": 404, "message": "Transaction ID not found"}
    return {"message": "Transaction retrieved", "data": MessageToDict(transaction)}

@transaction.post("/transactions/create")
async def create_transaction(transaction: TransactionCreation):
    newTransaction = await createTransaction(transaction)
    if newTransaction is None or newTransaction.transactionId == "":
        return {"status": 500, "message": "Error occured"}
    return {"message": "Transaction created", "data": MessageToDict(newTransaction)}

