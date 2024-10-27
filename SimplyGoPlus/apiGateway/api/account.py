from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ...generated import account_pb2_grpc, account_pb2
from google.protobuf.json_format import MessageToJson, MessageToDict
import grpc
import json

ACCOUNT_SERVICE_ADDRESS = "localhost:50051"

class Account(BaseModel):
    name: str 
    nric: str 
    username: str
    
class AccountCreation(Account):
    password: str
    
class AccountResponse(Account):
    userid: str
    password: str
    accountStatus: str
    walletId: str | None = None
    
account = APIRouter()

async def getAccount(accountId: str) -> account_pb2.AccountResponse:
    async with grpc.aio.insecure_channel(ACCOUNT_SERVICE_ADDRESS) as channel:
        stub = account_pb2_grpc.AccountStub(channel)
        try:
            response = await stub.GetAccount(account_pb2.AccountRequest(userId=accountId))
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
                password=account.password
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
            raise HTTPException(status_code=500, detail=f"gRPC error: {e.details()}")

async def deleteAccount(accountId: str) -> None:
    async with grpc.aio.insecure_channel(ACCOUNT_SERVICE_ADDRESS) as channel:
        stub = account_pb2_grpc.AccountStub(channel)
        try:
            await stub.DeleteAccount(account_pb2.AccountRequest(userId=accountId))
        except grpc.aio.AioRpcError as e:
            raise HTTPException(status_code=500, detail=f"gRPC error: {e.details()}")

@account.get("/accounts/{accountId}")
async def get_account(accountId: str):
    account = await getAccount(accountId)
    return {"message": "Account retrieved", "data": MessageToDict(account)}

@account.post("/accounts/create")
async def create_account(account: AccountCreation):
    newAccount = await createAccount(account)
    return {"message": "Account created", "data": MessageToDict(newAccount)}

@account.put("/accounts/{accountId}")
async def update_account(accountId: str, account: Account):
    updatedAccount = await updateAccount(accountId, account)
    return {"message": "Account updated", "data": MessageToDict(updatedAccount)}

@account.delete("/accounts/{accountId}")
async def delete_account(accountId: str):
    await deleteAccount(accountId)
    return {"message": "Account deleted successfully"}