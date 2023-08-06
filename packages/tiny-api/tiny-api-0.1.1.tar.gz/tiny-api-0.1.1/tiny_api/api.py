from webob import Response
from .Requests import Request
from parse import parse
import inspect
import os
from jinja2 import Environment, FileSystemLoader
from whitenoise import WhiteNoise
from .middleware import Middleware
from .constants import METHODS
from typing import Any,Callable


class Tinyapi:

    def __init__(self,templates_dir="templates",static_dir="static") -> None:
        self.routes = {}
        self.templates_env = Environment(loader= FileSystemLoader(os.path.abspath(templates_dir)))
        self.exception_handler = None
        self.whitenoise = WhiteNoise(self.wsgi_app,root= static_dir)
        self.middleware = Middleware(self)

    def __call__(self,environ:dict, start_response:Callable, *args:Any, **kwrgs:Any)-> Any:
        path_info = environ["PATH_INFO"]
        
        # if the url starts with 'static' then let it be served by Whitenoise
        # Here Whitenoise wraps the app as middleware does
        if path_info.startswith('/static'):

            environ["PATH_INFO"] = path_info[len("/static"):]
            return self.whitenoise(environ, start_response)

        return self.middleware(environ, start_response)


    def add_middleware(self,middleware_cls:Callable) -> None:
        """
        add a middleware class to your app
        """
        self.middleware.add(middleware_cls)

    def wsgi_app(self,environ:dict,start_response:Callable) -> Response:
        """
        a basic wsgi app, basically created for Whitenoise(middleware) to handle static files
        """
        request = Request(environ)
        response = self.handle_request(request)
        return response(environ,start_response)


    def template(self,template_name:str,context= None)-> Any:
        """
        for rendering templates
        """
        return self.templates_env.get_template(template_name).render(**context)

    
    def add_exception_handler(self,exception_handler:Callable) -> None:
        """
        Add your own custom exception handler.
        
        def custom_exception(request,response,exception_class):
            raise exception_class

        app.add_exception_handler(custom_exception)
        
        """
        self.exception_handler = exception_handler

    def route(self,path:str, allowed_methods = None)-> Callable:
        """
        A decorator function to handle routes in your app.
        """
        assert path not in self.routes, f"{path} route already exists"

        def wrapper(handler:Callable) -> Callable:  
            
            # if the route handler is a class
            if inspect.isclass(handler):
                http_methods = handler().ALLOWED_METHODS

                # if no ALLOWED_METHODS is specified in the class
                if http_methods is None:
                    http_methods = METHODS

            # if the route handler is a function
            else:

                # if no allowed_methods is specified in the function's argument
                if allowed_methods == None:
                    http_methods = METHODS
                
                else:
                    http_methods = allowed_methods

            # store the handler function/class inside an array
            handler_arr = [handler]
            handler_arr.extend(http_methods)  # appending the allowed methods for that handler in the same array

            # map route: [handler_arr,allowed_methods] and save in the routes dict
            self.routes[path] = handler_arr
            return handler_arr[0]

        return wrapper

    def handle_request(self,request:Request) -> Response:

        """
        Handles the request coming from the client.
        This gets called by the middeware or whitenoise(which also acts like a middleware)
        """

        response = Response()

        handler_arr,kwargs = self.find_handler(request.path)

        try:
            if handler_arr is not None:

                # for class based views
                if inspect.isclass(handler_arr[0]):
                    if request.method in handler_arr:  # for allowed methods
                        handler = getattr(handler_arr[0](),request.method.lower(),None)
                        response = handler(request,**kwargs)

                    else:      # if the requested method isn't allowed
                        response.text = f"{request.method} method not allowed"
                        response.status_code = 400
                        print(f"{response.status_code} {response.text}")

                # for function based views
                else:
                    handler = handler_arr[0]
                    if str(request.method) in handler_arr:
                        response = handler(request,**kwargs)
                    else:
                        response.text = f"{request.method} method not allowed"
                        response.status_code = 400
                        print(f"{response.status_code} {response.text}")


                        # raise AttributeError("Method not allowed", request.method)

            # give 404 error message
            else:
                self.default_response(response)

        except Exception as e:
            if self.exception_handler is None:  
                raise e

            else:               # if custom exception is specified
                self.exception_handler(request,response,e)
        
        return response

    def find_handler(self,request_path:str) -> Any:
        """
        Finds the handler method for each requested path.
        If no handler is present, returns None
        """

        for path,handler_arr in self.routes.items():
            parse_result = parse(path,request_path)
            if parse_result is not None:
                return handler_arr, parse_result.named

        return None,None


    def default_response(self,response:Response) -> None:
        """
        method for handling 404 error
        """
        response.status_code = 404
        response.text = "Not Found"
