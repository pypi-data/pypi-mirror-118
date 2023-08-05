from datetime import datetime, timedelta
import jwt
import random
from .constants import SECRET_KEY, ALGORITHM
from .get_env_var import get_env_vars


def create_access_token(user_id,username,seconds,secret_key= None):
    """
    Use the proper SECRET_KEY you specified for your app while creating the access token.
    """
    secret_key = get_env_vars('SECRET_KEY',default=SECRET_KEY)
    
    expire = datetime.utcnow() + timedelta(seconds=seconds)

    to_encode = {
        'id' : user_id,
        'username': username,
        'exp': expire
    }
    access_token = jwt.encode(to_encode,key = secret_key, algorithm=ALGORITHM)
    return access_token


def decode_access_token(data,secret_key= None):
    """
    Decode your access token
    """

    secret_key = get_env_vars('SECRET_KEY',default=SECRET_KEY)

    try:
        token_data = jwt.decode(data, key = secret_key, algorithms=ALGORITHM)
        return True,token_data

    except Exception as e:
        return False, e


def create_refresh_token():
    return '1234' + str(random.randint(1,4)) + str(random.randint(4,9)) + str(random.randint(0,9))

