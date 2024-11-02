import asyncio
import logging
import grpc
from ..generated import account_pb2
from ..generated import account_pb2_grpc
from ..common.utils import generateRandomId
from .db import AccountDB

accountDB = AccountDB()

class Account(account_pb2_grpc.AccountServicer):
    async def GetAccountById(self, request: account_pb2.AccountRequestById, context: grpc.aio.ServicerContext) -> account_pb2.AccountResponse:
        account = accountDB.getAccountById(request.userId)
        if account is False:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Account not found or error occured.")
            return account_pb2.AccountResponse()
        return account_pb2.AccountResponse(
            userId=account["accountId"],
            name=account["name"],
            nric=account["nric"],
            username=account["username"],
            password=account["password"],
            accountStatus=account["accountStatus"],
            walletAmount=str(account["walletAmount"])
        )

    async def GetAccountByUsername(self, request: account_pb2.AccountRequestByUsername, context: grpc.aio.ServicerContext) -> account_pb2.AccountResponse:
        account = accountDB.getAccountByUsername(request.username)
        if account is False:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Account not found or error occured.")
            return account_pb2.AccountResponse()
        return account_pb2.AccountResponse(
            userId=account["accountId"],
            name=account["name"],
            nric=account["nric"],
            username=account["username"],
            password=account["password"],
            accountStatus=account["accountStatus"],
            walletAmount=str(account["walletAmount"])
        )
    async def CreateAccount(self, request: account_pb2.CreateAccountRequest, context: grpc.aio.ServicerContext) -> account_pb2.AccountResponse:
        newUserId = generateRandomId()
        account = accountDB.createAccount(
            (newUserId, request.name, request.nric, request.username, request.password, True, 0.0)
        )
        if account is False:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Account creation failed. Please try another username.")
            return account_pb2.AccountResponse()
        return account_pb2.AccountResponse(userId=newUserId)

    async def UpdateAccount(self, request: account_pb2.UpdateAccountRequest, context: grpc.aio.ServicerContext) -> account_pb2.AccountResponse:
        updated = accountDB.updateAccount(
            request.userId,
            {"name": request.name, "nric": request.nric, "password": request.password}
        )
        if not updated:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Account not found for update or error occured.")
            return account_pb2.AccountResponse()
        return account_pb2.AccountResponse(userId=request.userId)

    async def UpdateWalletAmount(self, request: account_pb2.UpdateWallet, context: grpc.aio.ServicerContext) -> account_pb2.UpdateWallet:
        updated = accountDB.updateWallet(
            request.userId,
            request.amount
        )
        if not updated:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Wallet not found for update or error occured.")
            return account_pb2.UpdateWallet()
        return account_pb2.UpdateWallet(userId=request.userId, amount=request.amount)

    async def DeleteAccount(self, request: account_pb2.AccountRequestById, context: grpc.aio.ServicerContext) -> account_pb2.AccountResponse:
        deleted = accountDB.deleteAccount(request.userId)
        if not deleted:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Account not found for deletion or error occured.")
        return account_pb2.AccountResponse()

async def serve() -> None:
    server = grpc.aio.server()
    account_pb2_grpc.add_AccountServicer_to_server(Account(), server)
    listen_addr = "[::]:50051"
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())
