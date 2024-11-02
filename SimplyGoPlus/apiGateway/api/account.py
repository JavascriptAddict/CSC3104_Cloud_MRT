from fastapi import APIRouter, Depends, UploadFile, Form, HTTPException
from ..models import Account, AccountCreation, AccountUpdate, AccountResponse, AccountTopUp
from ..auth import getCurrentUser
from google.protobuf.json_format import MessageToDict
from ..gRPCHandler import getAccountById, updateAccount, deleteAccount, createAccount, createEmbedding, updateUserWallet, updateEmbedding, getUserByImage
from ..utils import checkWalletAmount, simulateCardCharge
from ..utils import hashPassword
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
    verifyCard = simulateCardCharge(cardNumber=topUpInfo.cardNumber, cvv=topUpInfo.cvv, expiryMonth=topUpInfo.expiryMonth, expiryYear=topUpInfo.expiryYear)
    if not verifyCard[0]:
        raise HTTPException(status_code=400, detail=f"{verifyCard[1]}")
    newAmount = float(currentUser.walletAmount) + topUpInfo.amount
    # Update account wallet amount
    updatedAccount = await updateUserWallet(currentUser.userId, newAmount)
    return {"message": "Wallet top up successful", "data": MessageToDict(updatedAccount)}

@account.post("/accounts/create") 
async def create_account(image: UploadFile, name: str = Form, nric: str = Form, username: str = Form, password: str = Form): 
    fileBytes = await image.read()
    try: 
        account = await getUserByImage(fileBytes)
        if account:
            return {"message": "Account exist or error occured"}
    except HTTPException:
        pass
    accountObj = AccountCreation(name=name, username=username, password=hashPassword(password), nric=nric) 
    newAccount = await createAccount(accountObj) 
    response = await createEmbedding(fileBytes, newAccount.userId) 
    if newAccount is None or response is None:
        raise HTTPException(status_code=500, detail="Error occured")
    return {"message": "Account created", "data": MessageToDict(newAccount)}

@account.put("/accounts/image/upload")
async def update_account_embedding(image: UploadFile, currentUser: AccountResponse = Depends(getCurrentUser)):
    fileBytes = await image.read()
    try: 
        account = await getUserByImage(fileBytes)
        if account.userId != currentUser.userId:
            return {"message": "This face embedding belongs to another user."}
    except HTTPException:
        pass
    response = await updateEmbedding(fileBytes, currentUser.userId)
    if response is None:
        raise HTTPException(status_code=500, detail="Error occured")
    return {"message": "Account embedding updated", "data": MessageToDict(response)}

@account.put("/accounts/")
async def update_account(account: AccountUpdate, currentUser: AccountResponse = Depends(getCurrentUser)):
    if currentUser.password != account.password:
        account.password = hashPassword(account.password)
    updatedAccount = await updateAccount(currentUser.userId, account)
    if updatedAccount is None:
        raise HTTPException(status_code=500, detail="Error occured")
    return {"message": "Account updated", "data": MessageToDict(updatedAccount)}

@account.delete("/accounts/")
async def delete_account(currentUser: AccountResponse = Depends(getCurrentUser)):
    deletedAccount = await deleteAccount(currentUser.userId)
    if deletedAccount is None:
        raise HTTPException(status_code=500, detail="Error occured")
    return {"message": "Account deleted successfully"}