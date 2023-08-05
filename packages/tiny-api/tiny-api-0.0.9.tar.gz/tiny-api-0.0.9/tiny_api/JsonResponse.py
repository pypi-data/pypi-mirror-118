from webob import Response
import json

def JsonResponse(result:dict,status_code):
    response = Response()
    response.content_type = 'application/json'
    response.status_code = status_code
    response.text = json.dumps(result)
    return response

def TemplateResponse(app,template_name,context:dict):
    response = Response()
    response.content_type = 'text/html'
    response.text = app.template(template_name, context=context)
    return response