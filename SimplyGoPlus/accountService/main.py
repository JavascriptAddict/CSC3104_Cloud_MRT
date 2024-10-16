# Copyright 2020 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
import logging
import grpc
from ..generated import account_pb2
from ..generated import account_pb2_grpc
from ..common.utils import generateRandomId
from .db import AccountDB

accountDB = AccountDB()

class Account(account_pb2_grpc.AccountServicer):
    async def GetAccount(
        self,
        request: account_pb2.AccountRequest,
        context: grpc.aio.ServicerContext,
    ) -> account_pb2.AccountResponse:
        account = accountDB.getAccount(request.userId)
        if account is None:
             return account_pb2.AccountResponse()
        return account_pb2.AccountResponse(userId=account["userId"], name=account["name"], 
                                           nric=account["nric"], username=account["username"], 
                                           password=account["password"], accountStatus=str(account["accountStatus"]), 
                                           walletId=account["walletId"])

    async def CreateAccount(
            self,
            request: account_pb2.AccountRequest,
            context: grpc.aio.ServicerContext,
        ) -> account_pb2.AccountResponse:
            newUserId = generateRandomId()
            newWalletId = generateRandomId()
            account = accountDB.createAccount((request.name, request.nric, request.username, request.password, True, newUserId, newWalletId))
            if account is None:
                return account_pb2.AccountResponse()
            return account_pb2.AccountResponse(userId=newUserId)
        
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
