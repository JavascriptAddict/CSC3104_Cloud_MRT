
from fastapi import APIRouter, UploadFile, HTTPException
from ..models import TripCreation, Trip, TransactionCreation
from ..auth import getCurrentUser
from google.protobuf.json_format import MessageToDict
from ..gRPCHandler import getAccountById, getUserByImage, createTrip, getTripByUserId, updateTrip, createTransaction, updateUserWallet
from ..utils import checkWalletAmount, generateRandomFare
import json

gantry = APIRouter()

@gantry.post("/gantry/tripStart")
async def start_trip(image: UploadFile, entry: str):
    fileBytes = await image.read()
    account = await getUserByImage(fileBytes)
    try:
        existingTrip = await getTripByUserId(account.userId)
        if existingTrip:
            return {"message": "There is already an ongoing trip with this user. Unable to start trip.", "data": MessageToDict(existingTrip)}
    except HTTPException:
        pass
    account = await getAccountById(account.userId)
    if not checkWalletAmount(account.walletAmount):
        return {"message": "Insufficient wallet amount", "data": account.walletAmount}
    newTrip = TripCreation(accountId=account.userId, entry=entry)
    startTrip = await createTrip(newTrip)
    if startTrip is None or startTrip.tripId == "":
        raise HTTPException(status_code=500, detail="Error occured")
    return {"message": "Trip created", "data": MessageToDict(startTrip)}

@gantry.put("/gantry/tripEnd")
async def end_trip(image: UploadFile, exit: str):
    fileBytes = await image.read()
    account = await getUserByImage(fileBytes)
    account = await getAccountById(account.userId)
    existingTrip = await getTripByUserId(account.userId)
    tripFare = generateRandomFare()
    newAmount = float(account.walletAmount) - tripFare
    updatedWallet = await updateUserWallet(account.userId, newAmount)
    newTransaction = TransactionCreation(accountId=account.userId, amount=tripFare)
    endTrip = Trip(entry=existingTrip.entry, exit=exit)
    updatedTrip = await updateTrip(existingTrip.tripId, endTrip)
    submittedTransaction = await createTransaction(newTransaction)
    if updatedTrip is None or submittedTransaction is None or updatedWallet is None:
        raise HTTPException(status_code=500, detail="Error occured")
    return  {"message": "Trip ended", "data": MessageToDict(updatedTrip)}