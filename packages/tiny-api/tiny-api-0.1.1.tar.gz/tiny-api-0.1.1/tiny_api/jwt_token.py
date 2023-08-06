from datetime import datetime, timedelta
from typing import Any
import jwt
from .constants import SECRET_KEY, ALGORITHM
from .get_env_var import get_env_vars
import uuid


def create_access_token(user_id:int, username:str, seconds:int, secret_key:str = None) -> str:
    """
    Use the proper SECRET_KEY you specified for your app while creating the access token.
    """
    if secret_key is None:
        secret_key = get_env_vars('SECRET_KEY',default=SECRET_KEY)
    
    expire = datetime.utcnow() + timedelta(seconds=seconds)

    to_encode = {
        'id' : user_id,
        'username': username,
        'exp': expire
    }
    access_token = jwt.encode(to_encode,key = secret_key, algorithm=ALGORITHM)
    return access_token


def decode_access_token(data:str, secret_key:str = None) -> Any:
    """
    Decode your access token
    """

    if secret_key is None:
        secret_key = get_env_vars('SECRET_KEY',default=SECRET_KEY)

    try:
        token_data = jwt.decode(data, key = secret_key, algorithms=ALGORITHM)
        return True,token_data

    except Exception as e:
        return False, e


def create_refresh_token() -> uuid.UUID:
    """
    It uses uuid4 to generate a random ID. You can use your own algorithm for  generating a refresh token.
    """
    return uuid.uuid4()
