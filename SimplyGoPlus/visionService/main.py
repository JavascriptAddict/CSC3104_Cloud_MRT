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
from ..generated import vision_pb2
from ..generated import vision_pb2_grpc
from .db import VisionDB
from .utils import compareFaces, getEmbeddingFromImage, pickleObject, unpickleObject

visionDB = VisionDB()

class Vision(vision_pb2_grpc.VisionServicer):
    async def GetUserId(self, request: vision_pb2.UserIdRequest, context: grpc.aio.ServicerContext) -> vision_pb2.UserIdResponse:
        vision = visionDB.getAllEmbeddings()
        userImage = request.image
        currentEmbedding = getEmbeddingFromImage(userImage)[0]
        if currentEmbedding is None:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("No face detected in image.")
            return vision_pb2.UserIdResponse()
        foundUser = False
        if vision is False:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("No embeddings found.")
            return vision_pb2.UserIdResponse()
        for i in vision:
            # Perform embedding comparison here
            knownEmbedding = unpickleObject(i[1])
            if knownEmbedding is None:
                print(i)
            if(compareFaces(knownEmbedding, currentEmbedding)):
                foundUser = i["userId"]
        if foundUser is False:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("User not found.")
            return vision_pb2.UserIdResponse()
        return vision_pb2.UserIdResponse(
            userId=foundUser,
        )

    async def CreateEmbedding(self, request: vision_pb2.CreateEmbeddingRequest, context: grpc.aio.ServicerContext) -> vision_pb2.EmbeddingActionResponse:
        # Convert to embedding here
        userImage = request.image
        currentEmbedding = getEmbeddingFromImage(userImage)[0]
        if currentEmbedding is None:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("No face detected in image.")
            return vision_pb2.EmbeddingActionResponse()
        pickledEmbedding = pickleObject(currentEmbedding)
        vision = visionDB.createEmbedding(
            (request.userId, pickledEmbedding)
        )
        if vision is False:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Embedding creation failed.")
            return vision_pb2.EmbeddingActionResponse()
        return vision_pb2.EmbeddingActionResponse(message="New embedding created.")

    async def UpdateEmbedding(self, request: vision_pb2.CreateEmbeddingRequest, context: grpc.aio.ServicerContext) -> vision_pb2.EmbeddingActionResponse:
        # Convert to embedding here
        userImage = request.image
        currentEmbedding = getEmbeddingFromImage(userImage)[0]
        if currentEmbedding is None:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("No face detected in image.")
            return vision_pb2.EmbeddingActionResponse()
        pickledEmbedding = pickleObject(currentEmbedding)
        updated = visionDB.updateEmbedding(
            request.userId,
            {"image": pickledEmbedding}
        )
        if not updated:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Embedding not found for update.")
            return vision_pb2.EmbeddingActionResponse()
        return vision_pb2.EmbeddingActionResponse(message="Embedding updated.")

    async def DeleteEmbedding(self, request: vision_pb2.DeleteEmbeddingRequest, context: grpc.aio.ServicerContext) -> vision_pb2.EmbeddingActionResponse:
        deleted = visionDB.deleteEmbedding(request.userId)
        if not deleted:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Embedding not found for deletion.")
        return vision_pb2.EmbeddingActionResponse(message="Embedding deleted.")

async def serve() -> None:
    server = grpc.aio.server()
    vision_pb2_grpc.add_VisionServicer_to_server(Vision(), server)
    listen_addr = "[::]:50054"
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())
