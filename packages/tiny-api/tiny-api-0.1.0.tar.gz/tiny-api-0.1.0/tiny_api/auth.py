from .jwt_token import decode_access_token
from .Responses import JsonResponse
from jwt.exceptions import InvalidSignatureError, InvalidTokenError, InvalidAlgorithmError, ExpiredSignatureError
from .constants import SECRET_KEY
from .get_env_var import get_env_vars
from .Requests import Request
from webob import Response
from typing import Any, Callable


def authenticated(func:Callable) -> Callable:

    secret_key = get_env_vars('SECRET_KEY',default=SECRET_KEY)

    def inner(request:Request ,*args:Any, **kwargs:Any) -> Response:

        bearer = request.bearer

        if  bearer is None:
            data = {
            'msg':"Access Token Missing. Authentication Required"
            }
            response = JsonResponse(data, 400)
        
        else:
            has_validity, token_data = decode_access_token(bearer,secret_key=secret_key)

            if has_validity:
                response = func(request,*args,**kwargs)
            
            else:
                token_data = token_data.__class__
                if token_data == ExpiredSignatureError:
                    data = {
                    'msg':" Access Token Has Expired. Authentication Required"
                    }
                    response = JsonResponse(data, 400)
            
                elif token_data == InvalidSignatureError:
                    data = {
                    'msg':" Invalid Access Token Signature"
                    }
                    response = JsonResponse(data, 400)

                elif token_data == InvalidTokenError:
                    data = {
                    'msg':" Invalid Access Token "
                    }
                    response = JsonResponse(data, 400)

                elif token_data ==  InvalidAlgorithmError:
                    data = {
                    'msg':" Invalid Access Token Algorithm"
                    }
                    response = JsonResponse(data, 400)       
        
        return response
    
    return inner


def is_authenticated(request: Request) -> bool:
    """
    check weather the requested user is authenticated or not
    """
    secret_key = get_env_vars('SECRET_KEY',default = SECRET_KEY)

    bearer = request.bearer

    if bearer is None:
        return False

    has_validity, _ = decode_access_token(bearer,secret_key)
    if has_validity:
        return True

    else:
        return False
            