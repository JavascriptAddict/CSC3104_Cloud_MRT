from fastapi import APIRouter
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

async def getAccount(accountId) -> None:
    async with grpc.aio.insecure_channel(ACCOUNT_SERVICE_ADDRESS) as channel:
        stub = account_pb2_grpc.AccountStub(channel)
        response = await stub.GetAccount(account_pb2.AccountRequest(userId=accountId))
    return response

async def createAccount(account) -> None:
    async with grpc.aio.insecure_channel(ACCOUNT_SERVICE_ADDRESS) as channel:
        stub = account_pb2_grpc.AccountStub(channel)
        response = await stub.CreateAccount(account_pb2.CreateAccountRequest(name=account.name, nric=account.nric, username=account.username, password=account.password))
    return response

@account.get("/accounts/{accountId}")
async def get_account(accountId: str):
    account = await getAccount(accountId)
    if account is None or account.userId == "":
        return {"status": 500, "message": "Error occured"}
    return {"message": "Account retrieved", "data": MessageToDict(account)}

@account.post("/accounts/create")
async def create_account(account: AccountCreation):
    newAccount = await createAccount(account)
    if newAccount is None or newAccount.userId == "":
        return {"status": 500, "message": "Error occured"}
    return {"message": "Account created", "data": MessageToDict(newAccount)}

