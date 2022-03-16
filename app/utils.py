# IMPORT DEENDENCIES
from datetime import datetime, timedelta
import string, random, jwt, sys
from app.exceptions import FileReadFailed
from typing import Optional
from app.config import settings
import pandas as pd

# DEFINE CHARACTERS USED IN TOKEN
uppercase_and_digits = string.ascii_uppercase + string.digits
lowercase_and_digits = string.ascii_lowercase + string.digits

# GENERATE ACCESS CODES
def gen_alphanumeric_code(length):
    code = ''.join((random.choice(uppercase_and_digits) for i in range(length)))
    return code

# CREATE ACCESS TOKEN
def create_token(data:dict, expires_delta:Optional[timedelta]=None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta # DEFINE EXPIRY DATE FOR ACCESS TOKEN
    else:
        expire = datetime.utcnow() + timedelta(minutes=30) # EXPIRES 30 MINUTES AFTER CREATION
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM) # GET SECRET KEY FOR TOKEN FROM CONFIG.PY
    return encoded_jwt

# DECRYPT ACCESS TOKEN
def decode_token(*, data:str):
    to_decode = data
    return jwt.decode(to_decode, settings.SECRET_KEY, algorithm=settings.ALGORITHM) # GET SECRET KEY FOR TOKEN FROM CONFIG.PY

# GET XCL FILE CONTENTS
async def read_xcl_file_contents(file, header):
    file = await file.read()
    try:
        return pd.read_excel(file, names=header)
    except ValueError:
        raise ValueError
    except:
        raise FileReadFailed('{}'.format(sys.exc_info()[0]))

# READ CSV FILE CONTENTS
async def read_csv_file_contents(file, header):
    file = await file.read()
    try:
        return pd.read_excel(file, names=header)
    except ValueError:
        raise ValueError
    except:
        raise FileReadFailed()

# BOOLEAN LOGIC
def logical_xor(a, b):
    return bool(a) ^ bool(b)

# GET PAIR COMBINATIONS FOR ACCESS TOKEN
def get_list_pairs(list1, list2, index:int=0):
    combination = []
    for i1 in list1:
        for i2 in list2:
            combination.append((i1,i2, str(gen_2_pow_n(index))))
            index+=1
    return combination

# GENERATE POW
def gen_2_pow_n(pow):
    return 2**pow

# TIME-STAMP
def timestamp_to_datetime(timestamp):
    dt_obj = datetime.fromtimestamp(timestamp)
    return dt_obj
