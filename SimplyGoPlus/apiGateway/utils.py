import bcrypt

MINIMUM_WALLET_AMOUNT = 2.50

def hashPassword(password: str) -> str:
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')

def checkWalletAmount(data):
    return float(data) > MINIMUM_WALLET_AMOUNT