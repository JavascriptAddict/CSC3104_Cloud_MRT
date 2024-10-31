from fastapi import APIRouter, Depends, UploadFile
from ..models import Account, AccountCreation, AccountResponse, AccountTopUp
from ..auth import getCurrentUser
from google.protobuf.json_format import MessageToDict
from ..gRPCHandler import getAccountById, updateAccount, deleteAccount, createAccount, createEmbedding, updateUserWallet
from ..utils import checkWalletAmount
import json

MINIMUM_WALLET_AMOUNT = 5.00

account = APIRouter()

@account.get("/accounts/")
async def get_account(currentUser: AccountResponse = Depends(getCurrentUser)):
    account = await getAccountById(currentUser.userId)
    return {"message": "Account retrieved", "data": MessageToDict(account)}

@account.get("/accounts/checkwallet/")
async def check_account_wallet(currentUser: AccountResponse = Depends(getCurrentUser)):
    account = await getAccountById(currentUser.userId)
    data = MessageToDict(account)
    walletAmount = data["walletAmount"]
    walletState = checkWalletAmount(walletAmount)
    return {"message": walletState, "data": walletAmount}

@account.post("/accounts/topup")
async def top_up(topUpInfo: AccountTopUp, currentUser: AccountResponse = Depends(getCurrentUser)):
    # Implement payment stuff here
    newAmount = float(currentUser.walletAmount) + topUpInfo.amount
    # Update account wallet amount
    updatedAccount = await updateUserWallet(currentUser.userId, newAmount)
    return {"message": "Wallet top up successful", "data": MessageToDict(updatedAccount)}

@account.post("/accounts/create")
async def create_account(account: AccountCreation):
    newAccount = await createAccount(account)
    return {"message": "Account created", "data": MessageToDict(newAccount)}

@account.post("/accounts/image/upload")
async def create_account_embedding(image: UploadFile, currentUser: AccountResponse = Depends(getCurrentUser)):
    fileBytes = await image.read()
    response = await createEmbedding(fileBytes, currentUser.userId)
    return {"message": "Account embedding created", "data": MessageToDict(response)}

@account.put("/accounts/")
async def update_account(account: Account, currentUser: AccountResponse = Depends(getCurrentUser)):
    updatedAccount = await updateAccount(currentUser.userId, account)
    return {"message": "Account updated", "data": MessageToDict(updatedAccount)}

@account.delete("/accounts/")
async def delete_account(currentUser: AccountResponse = Depends(getCurrentUser)):
    await deleteAccount(currentUser.userId)
    return {"message": "Account deleted successfully"}