from ..generated import account_pb2_grpc, account_pb2, transaction_pb2, transaction_pb2_grpc, trip_pb2, trip_pb2_grpc, vision_pb2, vision_pb2_grpc
from .models import Account, AccountCreation, AccountUpdate, Transaction, Trip, TripCreation, TripResponse
from fastapi import HTTPException
from dotenv import load_dotenv
import grpc
import os

load_dotenv()

ACCOUNT_SERVICE_ADDRESS = os.getenv('ACCOUNT_SERVICE_ADDRESS') 
TRANSACTION_SERVICE_ADDRESS = os.getenv('TRANSACTION_SERVICE_ADDRESS') 
TRIP_SERVICE_ADDRESS = os.getenv('TRIP_SERVICE_ADDRESS') 
VISION_SERVICE_ADDRESS = os.getenv('VISION_SERVICE_ADDRESS') 

async def getAccountById(accountId: str) -> account_pb2.AccountResponse:
    async with grpc.aio.insecure_channel(ACCOUNT_SERVICE_ADDRESS) as channel:
        stub = account_pb2_grpc.AccountStub(channel)
        try:
            response = await stub.GetAccountById(account_pb2.AccountRequestById(userId=accountId))
            return response
        except grpc.aio.AioRpcError as e:
            raise HTTPException(status_code=404, detail=f"Error: {e.details()}")


async def getAccountByUsername(accountUsername: str) -> account_pb2.AccountResponse:
    async with grpc.aio.insecure_channel(ACCOUNT_SERVICE_ADDRESS) as channel:
        stub = account_pb2_grpc.AccountStub(channel)
        try:
            response = await stub.GetAccountByUsername(account_pb2.AccountRequestByUsername(username=accountUsername))
            return response
        except grpc.aio.AioRpcError as e:
            raise HTTPException(status_code=404, detail=f"Error: {e.details()}")
        
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
            raise HTTPException(status_code=500, detail=f"Error: {e.details()}")

async def updateAccount(accountId: str, account: AccountUpdate) -> account_pb2.AccountResponse:
    async with grpc.aio.insecure_channel(ACCOUNT_SERVICE_ADDRESS) as channel:
        stub = account_pb2_grpc.AccountStub(channel)
        try:
            response = await stub.UpdateAccount(account_pb2.UpdateAccountRequest(
                userId=accountId,
                name=account.name,
                nric=account.nric,
                password=account.password
            ))
            return response
        except grpc.aio.AioRpcError as e:
            raise HTTPException(status_code=500, detail=f"Error: {e.details()}")

async def updateUserWallet(accountId: str, amount: float) -> account_pb2.UpdateWallet:
    async with grpc.aio.insecure_channel(ACCOUNT_SERVICE_ADDRESS) as channel:
        stub = account_pb2_grpc.AccountStub(channel)
        try:
            response = await stub.UpdateWalletAmount(account_pb2.UpdateWallet(
                userId=accountId,
                amount=str(amount)
            ))
            return response
        except grpc.aio.AioRpcError as e:
            raise HTTPException(status_code=500, detail=f"Error: {e.details()}")
                      
async def deleteAccount(accountId: str) -> None:
    async with grpc.aio.insecure_channel(ACCOUNT_SERVICE_ADDRESS) as channel:
        stub = account_pb2_grpc.AccountStub(channel)
        try:
            response = await stub.DeleteAccount(account_pb2.AccountRequestById(userId=accountId))
            print(response)
            return response
        except grpc.aio.AioRpcError as e:
            raise HTTPException(status_code=500, detail=f"Error: {e.details()}")


async def getTransaction(userId: str) -> transaction_pb2.TransactionList:
    async with grpc.aio.insecure_channel(TRANSACTION_SERVICE_ADDRESS) as channel:
        stub = transaction_pb2_grpc.TransactionStub(channel)
        try:
            response = await stub.GetTransaction(transaction_pb2.TransactionRequest(userId=userId))
            return response
        except grpc.aio.AioRpcError as e:
            raise HTTPException(status_code=404, detail=f"Error: {e.details()}")

async def createTransaction(transaction: Transaction) -> transaction_pb2.TransactionResponse:
    async with grpc.aio.insecure_channel(TRANSACTION_SERVICE_ADDRESS) as channel:
        stub = transaction_pb2_grpc.TransactionStub(channel)
        try:
            response = await stub.CreateTransaction(transaction_pb2.CreateTransactionRequest(amount=transaction.amount, accountId=transaction.accountId))
            return response
        except grpc.aio.AioRpcError as e:
            raise HTTPException(status_code=500, detail=f"Error: {e.details()}")

async def updateTransaction(transactionId: str, transaction: Transaction) -> transaction_pb2.TransactionResponse:
    async with grpc.aio.insecure_channel(TRANSACTION_SERVICE_ADDRESS) as channel:
        stub = transaction_pb2_grpc.TransactionStub(channel)
        try:
            response = await stub.UpdateTransaction(transaction_pb2.UpdateTransactionRequest(amount=transaction.amount, transactionId=transactionId))
            return response
        except grpc.aio.AioRpcError as e:
            raise HTTPException(status_code=500, detail=f"Error: {e.details()}")


async def createTrip(trip: TripCreation) -> trip_pb2.TripResponse:
    async with grpc.aio.insecure_channel(TRIP_SERVICE_ADDRESS) as channel:
        stub = trip_pb2_grpc.TripStub(channel)
        try:
            response = await stub.CreateTrip(trip_pb2.CreateTripRequest(
                accountId=trip.accountId,
                entry=trip.entry,
                exit=trip.exit,
            ))
            return response
        except grpc.aio.AioRpcError as e:
            raise HTTPException(status_code=500, detail=f"Error: {e.details()}")

async def getTrips(userId: str) -> trip_pb2.TripResponse:
    async with grpc.aio.insecure_channel(TRIP_SERVICE_ADDRESS) as channel:
        stub = trip_pb2_grpc.TripStub(channel)
        try:
            response = await stub.GetTrip(trip_pb2.TripRequest(userId=userId))
            return response
        except grpc.aio.AioRpcError as e:
            raise HTTPException(status_code=404, detail=f"Error: {e.details()}")

async def getTripByUserId(userId: str) -> trip_pb2.TripResponse:
    async with grpc.aio.insecure_channel(TRIP_SERVICE_ADDRESS) as channel:
        stub = trip_pb2_grpc.TripStub(channel)
        try:
            response = await stub.GetTripByUserId(trip_pb2.TripRequest(userId=userId))
            return response
        except grpc.aio.AioRpcError as e:
            raise HTTPException(status_code=404, detail=f"Error: {e.details()}")
    
async def updateTrip(tripId: str, trip: Trip) -> trip_pb2.TripResponse:
    async with grpc.aio.insecure_channel(TRIP_SERVICE_ADDRESS) as channel:
        stub = trip_pb2_grpc.TripStub(channel)
        try:
            response = await stub.UpdateTrip(trip_pb2.UpdateTripRequest(
                tripId=tripId,
                entry=trip.entry,
                exit=trip.exit,
            ))
            return response
        except grpc.aio.AioRpcError as e:
            raise HTTPException(status_code=500, detail=f"Error: {e.details()}")

async def getUserByImage(userImage: bytes) -> vision_pb2.UserIdResponse:
    async with grpc.aio.insecure_channel(VISION_SERVICE_ADDRESS) as channel:
        stub = vision_pb2_grpc.VisionStub(channel)
        try:
            response = await stub.GetUserId(vision_pb2.UserIdRequest(image=userImage))
            return response
        except grpc.aio.AioRpcError as e:
            raise HTTPException(status_code=404, detail=f"Error: {e.details()}")
        
async def createEmbedding(userImage: bytes, userId: str) -> vision_pb2.EmbeddingActionResponse:
    async with grpc.aio.insecure_channel(VISION_SERVICE_ADDRESS) as channel:
        stub = vision_pb2_grpc.VisionStub(channel)
        try:
            response = await stub.CreateEmbedding(vision_pb2.CreateEmbeddingRequest(userId=userId, image=userImage))
            return response
        except grpc.aio.AioRpcError as e:
            raise HTTPException(status_code=500, detail=f"Error: {e.details()}")

async def updateEmbedding(userImage: bytes, userId: str) -> vision_pb2.EmbeddingActionResponse:
    async with grpc.aio.insecure_channel(VISION_SERVICE_ADDRESS) as channel:
        stub = vision_pb2_grpc.VisionStub(channel)
        try:
            response = await stub.UpdateEmbedding(vision_pb2.CreateEmbeddingRequest(userId=userId, image=userImage))
            return response
        except grpc.aio.AioRpcError as e:
            raise HTTPException(status_code=500, detail=f"Error: {e.details()}")
    
async def deleteEmbedding(userId: str) -> vision_pb2.EmbeddingActionResponse:
    async with grpc.aio.insecure_channel(VISION_SERVICE_ADDRESS) as channel:
        stub = vision_pb2_grpc.VisionStub(channel)
        try:
            response = await stub.DeleteEmbedding(vision_pb2.DeleteEmbeddingRequest(userId=userId))
            return response
        except grpc.aio.AioRpcError as e:
            raise HTTPException(status_code=500, detail=f"Error: {e.details()}")