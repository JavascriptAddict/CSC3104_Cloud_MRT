from fastapi import APIRouter
from ..gRPCHandler import getTrip, createTrip, updateTrip
from google.protobuf.json_format import MessageToJson, MessageToDict
from ..models import Trip, TripCreation

trip = APIRouter()

@trip.get("/trips/{tripId}")
async def get_trip(tripId: str):
    trip = await getTrip(tripId)
    if trip is None or trip.tripId == "":
        return {"status": 404, "message": "Trip ID not found"}
    return {"message": "Trip retrieved", "data": MessageToDict(trip)}

@trip.post("/trips/create")
async def create_trip(trip: TripCreation):
    newTrip = await createTrip(trip)
    if newTrip is None or newTrip.tripId == "":
        return {"status": 500, "message": "Error occurred"}
    return {"message": "Trip created", "data": MessageToDict(newTrip)}

@trip.put("/trips/update/{tripId}")
async def update_trip(tripId: str, trip: Trip):
    updatedTrip = await updateTrip(tripId, trip)
    if updatedTrip is None:
        return {"status": 500, "message": "Error occurred"}
    return  {"message": "Trip updated", "data": MessageToDict(updatedTrip)}
