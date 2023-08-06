from webob import Response
import json
from .api import Tinyapi


def JsonResponse(result:dict,status_code:int) -> Response:
    response = Response()
    response.content_type = 'application/json'
    response.status_code = status_code
    response.text = json.dumps(result)
    return response

def TemplateResponse(app:Tinyapi,template_name:str,context:dict) -> Response:
    response = Response()
    response.content_type = 'text/html'
    response.text = app.template(template_name, context=context)
    return response