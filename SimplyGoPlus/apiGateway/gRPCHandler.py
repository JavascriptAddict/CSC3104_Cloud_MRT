from ..generated import account_pb2_grpc, account_pb2, transaction_pb2, transaction_pb2_grpc
from .models import Account, AccountCreation, Transaction
from .utils import hashPassword
import grpc
from fastapi import HTTPException


ACCOUNT_SERVICE_ADDRESS = "localhost:50051"
TRANSACTION_SERVICE_ADDRESS = "localhost:50052"

async def getAccountById(accountId: str) -> account_pb2.AccountResponse:
    async with grpc.aio.insecure_channel(ACCOUNT_SERVICE_ADDRESS) as channel:
        stub = account_pb2_grpc.AccountStub(channel)
        try:
            response = await stub.GetAccountById(account_pb2.AccountRequestById(userId=accountId))
            return response
        except grpc.aio.AioRpcError as e:
            raise HTTPException(status_code=500, detail=f"gRPC error: {e.details()}")


async def getAccountByUsername(accountUsername: str) -> account_pb2.AccountResponse:
    async with grpc.aio.insecure_channel(ACCOUNT_SERVICE_ADDRESS) as channel:
        stub = account_pb2_grpc.AccountStub(channel)
        try:
            response = await stub.GetAccountByUsername(account_pb2.AccountRequestByUsername(username=accountUsername))
            return response
        except grpc.aio.AioRpcError as e:
            raise HTTPException(status_code=500, detail=f"gRPC error: {e.details()}")
        
async def createAccount(account: AccountCreation) -> account_pb2.AccountResponse:
    async with grpc.aio.insecure_channel(ACCOUNT_SERVICE_ADDRESS) as channel:
        stub = account_pb2_grpc.AccountStub(channel)
        try:
            response = await stub.CreateAccount(account_pb2.CreateAccountRequest(
                name=account.name, 
                nric=account.nric, 
                username=account.username,
                password=hashPassword(account.password)
            ))
            return response
        except grpc.aio.AioRpcError as e:
            raise HTTPException(status_code=500, detail=f"gRPC error: {e.details()}")

async def updateAccount(accountId: str, account: Account) -> account_pb2.AccountResponse:
    async with grpc.aio.insecure_channel(ACCOUNT_SERVICE_ADDRESS) as channel:
        stub = account_pb2_grpc.AccountStub(channel)
        try:
            response = await stub.UpdateAccount(account_pb2.UpdateAccountRequest(
                userId=accountId,
                name=account.name,
                nric=account.nric,
                username=account.username
            ))
            return response
        except grpc.aio.AioRpcError as e:
            raise HTTPException(status_code=500, detail=f"gRPC error: {e.details()}")\
                
async def deleteAccount(accountId: str) -> None:
    async with grpc.aio.insecure_channel(ACCOUNT_SERVICE_ADDRESS) as channel:
        stub = account_pb2_grpc.AccountStub(channel)
        try:
            await stub.DeleteAccount(account_pb2.AccountRequestById(userId=accountId))
        except grpc.aio.AioRpcError as e:
            raise HTTPException(status_code=500, detail=f"gRPC error: {e.details()}")

# Initialize the gRPC channel and stub once
channel = grpc.aio.insecure_channel(TRANSACTION_SERVICE_ADDRESS)
stub = transaction_pb2_grpc.TransactionStub(channel)

async def getTransaction(transactionId: str) -> transaction_pb2.TransactionResponse:
    try:
        response = await stub.GetTransaction(transaction_pb2.TransactionRequest(transactionId=transactionId))
        return response
    except grpc.aio.AioRpcError as e:
        raise HTTPException(status_code=500, detail=f"gRPC error: {e.details()}")

async def createTransaction(transaction: Transaction) -> transaction_pb2.TransactionResponse:
    try:
        response = await stub.CreateTransaction(transaction_pb2.CreateTransactionRequest(amount=transaction.amount, walletId=transaction.walletId))
        return response
    except grpc.aio.AioRpcError as e:
        raise HTTPException(status_code=500, detail=f"gRPC error: {e.details()}")

async def updateTransaction(transactionId: str, transaction: Transaction) -> transaction_pb2.TransactionResponse:
    try:
        response = await stub.UpdateTransaction(transaction_pb2.UpdateTransactionRequest(amount=transaction.amount, walletId=transaction.walletId, transactionId=transactionId))
        return response
    except grpc.aio.AioRpcError as e:
        raise HTTPException(status_code=500, detail=f"gRPC error: {e.details()}")
