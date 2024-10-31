from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    userId: str
    
class Account(BaseModel):
    name: str 
    nric: str 
    username: str
    
class AccountCreation(Account):
    password: str
    
class AccountResponse(Account):
    userid: str
    password: str
    accountStatus: str
    walletId: str | None = None


class Transaction(BaseModel):
    amount: float

class TransactionCreation(Transaction):
    accountId: str

class TransactionResponse(Transaction):
    transactionId: str
    timestamp: str
    
    
class Trip(BaseModel):
    entry: str
    exit: str | None = None

class TripCreation(Trip):
    accountId: str

class TripResponse(Trip):
    tripId: str
    accountId: str
    timestamp: str
    

class Trip(BaseModel):
    entry: str
    exit: str | None = None

class TripCreation(Trip):
    accountId: str

class TripResponse(Trip):
    tripId: str
    accountId: str
    timestamp: str

