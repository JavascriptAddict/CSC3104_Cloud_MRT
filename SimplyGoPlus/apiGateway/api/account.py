from fastapi import APIRouter, Depends, UploadFile
from ..models import Account, AccountCreation, AccountResponse
from ..auth import getCurrentUser
from google.protobuf.json_format import MessageToDict
from ..gRPCHandler import getAccountById, updateAccount, deleteAccount, createAccount, createEmbedding
from ..utils import checkWalletAmount
import json

MINIMUM_WALLET_AMOUNT = 2.50

account = APIRouter()

@account.get("/accounts/{accountId}")
async def get_account(currentUser: AccountResponse = Depends(getCurrentUser)):
    account = await getAccountById(currentUser.userid)
    return {"message": "Account retrieved", "data": MessageToDict(account)}

@account.get("/accounts/checkwallet/{accountId}")
async def check_account_wallet(currentUser: AccountResponse = Depends(getCurrentUser)):
    account = await getAccountById(currentUser.userid)
    data = MessageToDict(account)
    walletAmount = data["walletAmount"]
    walletState = checkWalletAmount(walletAmount)
    return {"message": walletState, "data": walletAmount}

@account.post("/accounts/create")
async def create_account(account: AccountCreation):
    newAccount = await createAccount(account)
    return {"message": "Account created", "data": MessageToDict(newAccount)}

@account.post("/accounts/image/upload")
async def create_account_embedding(image: UploadFile, currentUser: AccountResponse = Depends(getCurrentUser)):
    fileBytes = await image.read()
    print("HEREH API")
    response = await createEmbedding(fileBytes, currentUser.userId)
    print(response)
    return {"message": "Account embedding created", "data": MessageToDict(response)}

@account.put("/accounts/")
async def update_account(account: Account, currentUser: AccountResponse = Depends(getCurrentUser)):
    updatedAccount = await updateAccount(currentUser.userid, account)
    return {"message": "Account updated", "data": MessageToDict(updatedAccount)}

@account.delete("/accounts/{accountId}")
async def delete_account(currentUser: AccountResponse = Depends(getCurrentUser)):
    await deleteAccount(currentUser.userid)
    return {"message": "Account deleted successfully"}