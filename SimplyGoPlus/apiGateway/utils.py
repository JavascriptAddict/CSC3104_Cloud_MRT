import bcrypt
import random
import re
from datetime import datetime

MINIMUM_WALLET_AMOUNT = 5

def hashPassword(password: str) -> str:
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')

def checkWalletAmount(data):
    return float(data) > MINIMUM_WALLET_AMOUNT

def generateRandomFare():
    return random.uniform(1.0, 5.0)

def simulateCardCharge(cardNumber, cvv, expiryMonth, expiryYear):
    expiryDate = f"{expiryMonth}/{expiryYear}"
    if not re.match(r'^\d{16}$', str(cardNumber)):
        return False, "Card number must be 16 digits"

    if not luhnAlgo(str(cardNumber)):
        return False, "Invalid card number"

    if not re.match(r'^\d{3}$', str(cvv)):
        return False, "CVV must be 3 digits"
    print(expiryDate)
    if not checkValidExpiry(expiryDate):
        return False, "Invalid expiration date"

    return True, "Payment successful"

def luhnAlgo(card_number):
    """Validate card number using Luhn algorithm."""
    total = 0
    reverse_digits = card_number[::-1]

    for i, digit in enumerate(reverse_digits):
        n = int(digit)
        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9
        total += n

    return total % 10 == 0

def checkValidExpiry(expiration_date):
    """Check if the expiration date is valid."""
    try:
        exp_date = datetime.strptime(expiration_date, "%m/%y")
        return exp_date > datetime.now()
    except ValueError:
        return False

