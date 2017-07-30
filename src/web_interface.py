from collections import defaultdict
from functools import lru_cache

from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config, notfound_view_config
import pyramid.httpexceptions as exc

import src.datasets
from src.generator import generate_from

PORT = 8080


@lru_cache(maxsize=1)
def quote_generator():
    return generate_from(src.datasets.donald_speech(n=4))


_quotes = defaultdict(lambda: next(quote_generator()))

def get_quote(quote_id):
    return _quotes[quote_id]

def next_quote_id():
    return len(_quotes)


@view_config(route_name='quote', renderer='../templates/quote.jinja2')
def quote(request):
    quote_id = request.matchdict.get('quote_id', '')

    if not quote_id.isdigit():
        return exc.HTTPNotFound()

    return {'quote': get_quote(quote_id) }

@view_config(route_name='root')
@view_config(route_name='next_quote')
def next_quote(request):
    return exc.HTTPFound(request.route_url('quote', quote_id=next_quote_id()))

def notfound(request):
    return exc.HTTPNotFound()

if __name__ == '__main__':
    with Configurator() as config:
        config.include('pyramid_jinja2')
        config.add_route('root', '/')
        config.add_route('quote', '/quote/{quote_id}/')
        config.add_route('next_quote', '/quote/')
        config.add_notfound_view(notfound, append_slash=True)
        config.scan()
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', PORT, app)
    server.serve_forever()
