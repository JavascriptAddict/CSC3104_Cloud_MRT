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