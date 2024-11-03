from fastapi import APIRouter, Depends
from ..gRPCHandler import getTrips, createTrip, updateTrip
from google.protobuf.json_format import MessageToJson, MessageToDict
from ..models import Trip, TripCreation, AccountResponse
from ..auth import getCurrentUser

trip = APIRouter()

@trip.get("/trips")
async def get_trip(currentUser: AccountResponse = Depends(getCurrentUser)):
    trips = MessageToDict(await getTrips(currentUser.userId))
    return {"message": "Trips retrieved", "data": trips}


