from os.path import defpath

# from .main import ACCOUNT_SERVICE_ADDRESS, TRANSACTION_SERVICE_ADDRESS, TRIP_SERVICE_ADDRESS
from ..generated import account_pb2_grpc, account_pb2, transaction_pb2, transaction_pb2_grpc, trip_pb2, trip_pb2_grpc, vision_pb2, vision_pb2_grpc
from .models import Account, AccountCreation, Transaction, Trip, TripCreation, TripResponse
from .utils import hashPassword
import grpc
from fastapi import HTTPException

ACCOUNT_SERVICE_ADDRESS = "localhost:50051"
TRANSACTION_SERVICE_ADDRESS = "localhost:50052"
TRIP_SERVICE_ADDRESS = "localhost:50053"
VISION_SERVICE_ADDRESS = "localhost:50054"

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
        print("here")
        try:
            print("here2")
            response = await stub.GetAccountByUsername(account_pb2.AccountRequestByUsername(username=accountUsername))
            print("here3")
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
            raise HTTPException(status_code=500, detail=f"gRPC error: {e.details()}")

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
            raise HTTPException(status_code=500, detail=f"gRPC error: {e.details()}")
                      
async def deleteAccount(accountId: str) -> None:
    async with grpc.aio.insecure_channel(ACCOUNT_SERVICE_ADDRESS) as channel:
        stub = account_pb2_grpc.AccountStub(channel)
        try:
            await stub.DeleteAccount(account_pb2.AccountRequestById(userId=accountId))
        except grpc.aio.AioRpcError as e:
            raise HTTPException(status_code=500, detail=f"gRPC error: {e.details()}")

# Initialize the gRPC channel and stub once
channel = grpc.aio.insecure_channel(TRANSACTION_SERVICE_ADDRESS)
transaction_stub = transaction_pb2_grpc.TransactionStub(channel)

async def getTransaction(userId: str) -> transaction_pb2.TransactionList:
    try:
        response = await transaction_stub.GetTransaction(transaction_pb2.TransactionRequest(userId=userId))
        return response
    except grpc.aio.AioRpcError as e:
        raise HTTPException(status_code=500, detail=f"gRPC error: {e.details()}")

async def createTransaction(transaction: Transaction) -> transaction_pb2.TransactionResponse:
    try:
        response = await transaction_stub.CreateTransaction(transaction_pb2.CreateTransactionRequest(amount=transaction.amount, accountId=transaction.accountId))
        return response
    except grpc.aio.AioRpcError as e:
        raise HTTPException(status_code=500, detail=f"gRPC error: {e.details()}")

async def updateTransaction(transactionId: str, transaction: Transaction) -> transaction_pb2.TransactionResponse:
    try:
        response = await transaction_stub.UpdateTransaction(transaction_pb2.UpdateTransactionRequest(amount=transaction.amount, transactionId=transactionId))
        return response
    except grpc.aio.AioRpcError as e:
        raise HTTPException(status_code=500, detail=f"gRPC error: {e.details()}")

# Initialize the gRPC channel and stub once
channel = grpc.aio.insecure_channel(TRIP_SERVICE_ADDRESS)
trip_stub = trip_pb2_grpc.TripStub(channel)

async def createTrip(trip: TripCreation) -> trip_pb2.TripResponse:
        try:
            response = await trip_stub.CreateTrip(trip_pb2.CreateTripRequest(
                accountId=trip.accountId,
                entry=trip.entry,
                exit=trip.exit,
            ))
            return response
        except grpc.aio.AioRpcError as e:
            raise HTTPException(status_code=500, detail=f"gRPC error: {e.details()}")

async def getTrips(userId: str) -> trip_pb2.TripResponse:
    try:
        response = await trip_stub.GetTrip(trip_pb2.TripRequest(userId=userId))
        return response
    except grpc.aio.AioRpcError as e:
        raise HTTPException(status_code=500, detail=f"gRPC error: {e.details()}")

async def getTripByUserId(userId: str) -> trip_pb2.TripResponse:
    try:
        response = await trip_stub.GetTripByUserId(trip_pb2.TripRequest(userId=userId))
        return response
    except grpc.aio.AioRpcError as e:
        raise HTTPException(status_code=500, detail=f"gRPC error: {e.details()}")
    
async def updateTrip(tripId: str, trip: Trip) -> trip_pb2.TripResponse:
    try:
        response = await trip_stub.UpdateTrip(trip_pb2.UpdateTripRequest(
            tripId=tripId,
            entry=trip.entry,
            exit=trip.exit,
        ))
        return response
    except grpc.aio.AioRpcError as e:
        raise HTTPException(status_code=500, detail=f"gRPC error: {e.details()}")

# Vision service
async def getUserByImage(userImage: bytes) -> vision_pb2.UserIdResponse:
    async with grpc.aio.insecure_channel(VISION_SERVICE_ADDRESS) as channel:
        stub = vision_pb2_grpc.VisionStub(channel)
        try:
            response = await stub.GetUserId(vision_pb2.UserIdRequest(image=userImage))
            return response
        except grpc.aio.AioRpcError as e:
            raise HTTPException(status_code=500, detail=f"gRPC error: {e.details()}")
        
async def createEmbedding(userImage: bytes, userId: str) -> vision_pb2.EmbeddingActionResponse:
    async with grpc.aio.insecure_channel(VISION_SERVICE_ADDRESS) as channel:
        stub = vision_pb2_grpc.VisionStub(channel)
        try:
            print("HERE API GATWAT")
            response = await stub.CreateEmbedding(vision_pb2.CreateEmbeddingRequest(userId=userId, image=userImage))
            return response
        except grpc.aio.AioRpcError as e:
            raise HTTPException(status_code=500, detail=f"gRPC error: {e.details()}")

async def updateEmbedding(userImage: bytes, userId: str) -> vision_pb2.EmbeddingActionResponse:
    async with grpc.aio.insecure_channel(VISION_SERVICE_ADDRESS) as channel:
        stub = vision_pb2_grpc.VisionStub(channel)
        try:
            response = await stub.UpdateEmbedding(vision_pb2.CreateEmbeddingRequest(userId=userId, image=userImage))
            return response
        except grpc.aio.AioRpcError as e:
            raise HTTPException(status_code=500, detail=f"gRPC error: {e.details()}")
    
async def deleteEmbedding(userId: str) -> vision_pb2.EmbeddingActionResponse:
    async with grpc.aio.insecure_channel(VISION_SERVICE_ADDRESS) as channel:
        stub = vision_pb2_grpc.VisionStub(channel)
        try:
            response = await stub.DeleteEmbedding(vision_pb2.DeleteEmbeddingRequest(userId=userId))
            return response
        except grpc.aio.AioRpcError as e:
            raise HTTPException(status_code=500, detail=f"gRPC error: {e.details()}")