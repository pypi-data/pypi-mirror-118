Tiny-api
--------

**Tiny-api is a python web framework for creating Restful APIs written for learning purpose out of curiosity.** 
**It is written with the help of** \ `Webob`_\ **, a library which provides** 
**objects for HTTP requests and responses.**

Installation
------------

Install using pip.

.. code:: sh

   $ pip3 install tiny-api

Getting Started
---------------

It’s really easy to get started with tiny-api.

.. code:: sh

       from tiny_api import Tinyapi
       from tiny_api.Responses import JsonResponse
       from tiny_api.Status import HTTP_200_OK

       app = Tinyapi()

       @app.route('/home')
       def home(request):
           return JsonResponse({'data':'hello world'},HTTP_200_OK)          

Important Links
---------------

1. Documentation :- https://kaushal-dhungel.github.io/tiny-api-docs
2. Documentation(github) :- https://github.com/Kaushal-Dhungel/tiny-api-docs
3. Pypi :- https://pypi.org/project/tiny-api/

Credits
-------

Thanks to Jahongir Rahmonov’s awesome blog that helped me get started
with this project. `Visit his blog`_

.. _Webob: https://docs.pylonsproject.org/projects/webob/en/stable/
.. _Visit his blog: https://rahmonov.me/posts/write-python-framework-part-one/
