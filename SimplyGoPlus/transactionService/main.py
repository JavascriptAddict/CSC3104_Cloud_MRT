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
import datetime
import logging
import grpc
from ..generated import transaction_pb2
from ..generated import transaction_pb2_grpc
from ..common.utils import generateRandomId
from .db import TransactionDB

transactionDB = TransactionDB()

class Transaction(transaction_pb2_grpc.TransactionServicer):
    async def GetTransaction(
        self,
        request: transaction_pb2.TransactionRequest,
        context: grpc.aio.ServicerContext,
    ) -> transaction_pb2.TransactionList:
        rows = transactionDB.getTransaction(request.userId)
        if rows is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("No transactions found for user or error occured.")
            return transaction_pb2.TransactionList()
        transactions = [transaction_pb2.TransactionResponse(transactionId=row["transactionId"], amount=row["amount"],
                                           accountId=row["accountId"], timestamp=row["timestamp"]) for row in rows]
        return transaction_pb2.TransactionList(transactions=transactions)

    async def CreateTransaction(
            self,
            request: transaction_pb2.TransactionRequest,
            context: grpc.aio.ServicerContext,
        ) -> transaction_pb2.TransactionResponse:
            newTransactionId = generateRandomId()
            timestamp = str(datetime.datetime.now())
            transaction = transactionDB.createTransaction((newTransactionId, request.amount, request.accountId, timestamp))
            if transaction is None:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Transaction creation failed or error occured.")
                return transaction_pb2.TransactionResponse()
            return transaction_pb2.TransactionResponse(transactionId=newTransactionId, amount = request.amount, accountId=request.accountId, timestamp=timestamp)

    async def UpdateTransaction(self, request: transaction_pb2.UpdateTransactionRequest, context: grpc.aio.ServicerContext) -> transaction_pb2.TransactionResponse:
        updated = transactionDB.updateTransaction(
            {"amount": request.amount, "transactionId": request.transactionId}
        )
        if not updated:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Transaction update failed or error occured.")
            return transaction_pb2.TransactionResponse()
        return transaction_pb2.TransactionResponse(transactionId=request.transactionId, amount=request.amount)


async def serve() -> None:
    server = grpc.aio.server()
    transaction_pb2_grpc.add_TransactionServicer_to_server(Transaction(), server)
    listen_addr = "[::]:50052"
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())
