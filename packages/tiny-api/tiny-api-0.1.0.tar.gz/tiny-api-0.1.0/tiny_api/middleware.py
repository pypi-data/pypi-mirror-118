from webob import Response
from .Requests import Request
from typing import Any, Callable

class Middleware:
    def __init__(self,app:Any) -> None:
        self.app = app

    def __call__(self,environ:dict,start_response:Callable, *args:Any, **kwargs:Any) -> Response:
        """
        The WSGI server talks to the middlerware first. Hence, it must follow wsgi standards.
        It must be a callable object and must receive 'environ' and 'start_response' 
        """

        request = Request(environ)
        request = self.tweak_request(request)
        response = self.app.handle_request(request)
        return response(environ,start_response)

    def tweak_request(self,request:Request) -> Request:
        try:
            bearer = request.authorization[1]
            if bearer is not None:
                request.bearer = bearer

            return request

        except Exception:
            return request

    
    def add(self,middleware_cls:Callable) -> None:
        """
        This adds a middleware to the app.
        This gets called by add_middleware method in api.py.
        """
        self.app = middleware_cls(self.app)

    def process_request(self, request:Request) -> None:
        """
        This must be overriden by the users, to tweak the request
        """
        pass

    def process_response(self, request:Request, response:Response) -> None:
        """
        This must be overriden by the users, to tweak the response
        """
        pass

    def handle_request(self,request:Request) -> Response:
        """
        This handles user's requests. 
        This calls the handle_request method of our app
        """
        self.process_request(request)
        response = self.app.handle_request(request)
        self.process_response(request,response)
        return response 

    