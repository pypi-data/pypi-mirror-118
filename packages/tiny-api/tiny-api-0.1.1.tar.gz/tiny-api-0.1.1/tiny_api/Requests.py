from webob import Request as WebobRequest
from .constants import SECRET_KEY
from typing import Any

class Request(WebobRequest):

    # user_params = {}
    # is_authenticated = False
    # user = 'AnonymousUser'
    # user_id = None
    # secret_key = SECRET_KEY


    def __init__(self, environ:dict, charset:Any = None, unicode_errors:Any = None, decode_param_names:Any = None, **kw:Any) -> None:

        super().__init__(environ, charset=charset, unicode_errors=unicode_errors, decode_param_names=decode_param_names, **kw)

        self.user_params = {}
        self.bearer = None
        # self.is_authenticated = False
        # self.secret_key = SECRET_KEY
        # self.user = 'AnonymousUser'
        # self.user_id = None


    def add_param(self,name:str,val:str) -> None:
        """
        Add your custom params to the request object
        """
        self.user_params[name] = val