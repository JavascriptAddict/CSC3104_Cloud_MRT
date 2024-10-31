from fastapi import APIRouter, Depends
from ..gRPCHandler import getTrips, createTrip, updateTrip
from google.protobuf.json_format import MessageToJson, MessageToDict
from ..models import Trip, TripCreation, AccountResponse
from ..auth import getCurrentUser

trip = APIRouter()

@trip.get("/trips")
async def get_trip(currentUser: AccountResponse = Depends(getCurrentUser)):
    trips = MessageToDict(await getTrips(currentUser.userId))
    if len(trips) < 1:
        return {"status": 404, "message": "No trips found"}
    return {"message": "Transaction retrieved", "data": trips}

# @trip.post("/trips/create")
# async def create_trip(trip: TripCreation):
#     newTrip = await createTrip(trip)
#     if newTrip is None or newTrip.tripId == "":
#         return {"status": 500, "message": "Error occurred"}
#     return {"message": "Trip created", "data": MessageToDict(newTrip)}

# @trip.put("/trips/update/{tripId}")
# async def update_trip(tripId: str, trip: Trip):
#     updatedTrip = await updateTrip(tripId, trip)
#     if updatedTrip is None:
#         return {"status": 500, "message": "Error occurred"}
#     return  {"message": "Trip updated", "data": MessageToDict(updatedTrip)}
