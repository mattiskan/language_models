from functools import lru_cache

from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config

import src.datasets
from src.generator import generate_from

PORT = 8080


@lru_cache(maxsize=1)
def generator():
    return generate_from(src.datasets.donald_speech(n=4))


responses = {}

@view_config(
    route_name='home'
)
def home(request):
    sentence = next(generator())
    print(sentence)
    
    return Response(sentence)


if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('home', '/')
        config.scan()
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', PORT, app)
    server.serve_forever()
