from jwt.exceptions import InvalidSignatureError
from webob import Request, Response
from Requests import Request
from jwt_token import decode_access_token

class Middleware:
    def __init__(self,app) -> None:
        self.app = app

    def __call__(self,environ,start_response, *args, **kwds):
        """
        The WSGI server talks to the middlerware first. Hence, it must follow wsgi standards.
        It must be a callable object and must receive 'environ' and 'start_response' 
        """
        # request = Request(environ)
        request = Request(environ)
        request = self.tweak_request(request)
        response = self.app.handle_request(request)
        return response(environ,start_response)

    def tweak_request(self,request):
        try:
            bearer = request.authorization[1]
            if bearer is not None:
                request.bearer = bearer

            return request

        except Exception:
            return request

    
    def add(self,middleware_cls):
        """
        This adds a middleware to the app.
        This gets called by add_middleware method in api.py.
        """
        self.app = middleware_cls(self.app)

    def process_request(self, request):
        """
        This must be overriden by the users, to tweak the request
        """
        pass

    def process_response(self, request, response):
        """
        This must be overriden by the users, to tweak the response
        """
        pass

    def handle_request(self,request):
        """
        This handles user's requests. 
        This calls the handle_request method of our app
        """
        self.process_request(request)
        response = self.app.handle_request(request)
        self.process_response(request,response)
        return response 

    