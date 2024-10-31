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
from ..generated import trip_pb2
from ..generated import trip_pb2_grpc
from ..common.utils import generateRandomId
from .tripService_db import TripDB

tripDB = TripDB()

class Trip(trip_pb2_grpc.TripServicer):
    async def GetTrip(
        self,
        request: trip_pb2.TripRequest,
        context: grpc.aio.ServicerContext,
    ) -> trip_pb2.TripResponse:
        trip = tripDB.getTrip(request.tripId)
        if trip is None:
             return trip_pb2.TripResponse()
        return trip_pb2.TripResponse(tripId=trip["tripId"], accountId=trip["accountId"], entry=trip["entry"],
                                           exit=trip["exit"], timestamp=trip["timestamp"])

    async def CreateTrip(
            self,
            request: trip_pb2.TripRequest,
            context: grpc.aio.ServicerContext,
        ) -> trip_pb2.TripResponse:
            newTripId = generateRandomId()
            timestamp = str(datetime.datetime.now())
            trip = tripDB.createTrip((newTripId, request.accountId, request.entry, request.exit, timestamp))
            if trip is None:
                return trip_pb2.TripResponse()
            return trip_pb2.TripResponse(tripId=newTripId, accountId=request.accountId, entry = request.entry, exit=request.exit, timestamp=timestamp)

    async def UpdateTrip(self, request: trip_pb2.UpdateTripRequest, context: grpc.aio.ServicerContext) -> trip_pb2.TripResponse:
        updated = tripDB.updateTrip(
            {"entry": request.entry, "exit": request.exit, "tripId": request.tripId}
        )
        if not updated:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Trip not found for update.")
            return trip_pb2.TripResponse()
        return trip_pb2.TripResponse(tripId=request.tripId, entry=request.entry,exit=request.exit)


async def serve() -> None:
    server = grpc.aio.server()
    trip_pb2_grpc.add_TripServicer_to_server(Trip(), server)
    listen_addr = "[::]:50053"
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())