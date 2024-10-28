from fastapi import APIRouter, Depends
from ..models import Account, AccountCreation, AccountResponse
from ..auth import getCurrentUser
from google.protobuf.json_format import MessageToDict
from ..gRPCHandler import getAccountById, updateAccount, deleteAccount, createAccount
import json

MINIMUM_WALLET_AMOUNT = 2.50

account = APIRouter()

def checkWalletAmount(data):
    return float(data) > MINIMUM_WALLET_AMOUNT

@account.get("/accounts/{accountId}")
async def get_account(accountId: str, currentUser: AccountResponse = Depends(getCurrentUser)):
    account = await getAccountById(accountId)
    return {"message": "Account retrieved", "data": MessageToDict(account)}

@account.get("/accounts/checkwallet/{accountId}")
async def check_account_wallet(accountId: str, currentUser: AccountResponse = Depends(getCurrentUser)):
    account = await getAccountById(accountId)
    data = MessageToDict(account)
    walletAmount = data["walletAmount"]
    walletState = checkWalletAmount(walletAmount)
    return {"message": walletState, "data": walletAmount}

@account.post("/accounts/create")
async def create_account(account: AccountCreation):
    newAccount = await createAccount(account)
    return {"message": "Account created", "data": MessageToDict(newAccount)}

@account.put("/accounts/{accountId}")
async def update_account(accountId: str, account: Account, currentUser: AccountResponse = Depends(getCurrentUser)):
    updatedAccount = await updateAccount(accountId, account)
    return {"message": "Account updated", "data": MessageToDict(updatedAccount)}

@account.delete("/accounts/{accountId}")
async def delete_account(accountId: str, currentUser: AccountResponse = Depends(getCurrentUser)):
    await deleteAccount(accountId)
    return {"message": "Account deleted successfully"}