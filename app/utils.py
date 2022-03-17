# IMPORT DEENDENCIES
import random
import string
from datetime import datetime, timedelta
from typing import Optional

import jwt

from app.config import settings

# DEFINE CHARACTERS USED IN TOKEN
uppercase_and_digits = string.ascii_uppercase + string.digits
lowercase_and_digits = string.ascii_lowercase + string.digits


# GENERATE ACCESS CODES
def gen_alphanumeric_code(length):
    code = ''.join((random.choice(uppercase_and_digits)
                   for i in range(length)))
    return code


# CREATE ACCESS TOKEN
def create_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        # DEFINE EXPIRY DATE FOR ACCESS TOKEN
        expire = datetime.utcnow() + expires_delta
    else:
        # EXPIRES 30 MINUTES AFTER CREATION
        expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    # GET SECRET KEY FOR TOKEN FROM CONFIG.PY
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


# DECRYPT ACCESS TOKEN
def decode_token(*, data: str):
    to_decode = data
    # GET SECRET KEY FOR TOKEN FROM CONFIG.PY
    return jwt.decode(to_decode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
