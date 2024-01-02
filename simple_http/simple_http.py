from typing import Callable
from simple_http import constants
from dataclasses import dataclass
from urllib.parse import parse_qs

@dataclass
class Route:
    path: str
    method: str
    handler: Callable


class BasicWSGIServer:
    def __init__(self):
        self.routes = []
        self.middleware = []

    def route(self, path, method="GET"):
        def decorator(func):
            self.routes.append(Route(path, method, func))
            return func
        return decorator

    def register_middleware(self, middleware_func):
        self.middleware.append(middleware_func)

    def use_middleware(self, environ):
        for middleware_func in self.middleware:
            middleware_func(environ)

    def get_route(self, environ):
        path = environ["PATH_INFO"]
        return next((route for route in self.routes if route.path == path), None)

    def method_allowed(self, environ):
        method = environ["REQUEST_METHOD"]
        route = self.get_route(environ)
        return method == route.method

    def get_response_data(self, environ):
        route = self.get_route(environ)
        if not route:
            response_body = "Not Found"
            status = constants.status_code_404

        # Probably a better idea to raise an exception here.
        elif not self.method_allowed(environ):
            response_body = "Method Not Allowed"
            status = constants.status_code_405

        else:
            response_body = route.handler(environ)
            if route.method == "POST":
                status = constants.status_code_201
            else:
                status = constants.status_code_200
        return response_body, status

    def __call__(self, environ, start_response):
        if query_string := environ.get("QUERY_STRING"):
            environ['query_string'] = parse_qs(query_string)

        environ['post_body'] = handle_body_data(environ)

        self.use_middleware(environ)

        response_body, status = self.get_response_data(environ)

        default_headers = [("Content-type", "text/plain")]
        start_response(status, default_headers)
        return [response_body.encode("utf-8")]


def handle_body_data(environ):
    # Temporary solution, we'll see how to handle this better later.
    try:
        request_body_size = int(environ.get("CONTENT_LENGTH", 0))
    except ValueError:
        request_body_size = 0

    input = environ["wsgi.input"]
    request_body = input.read(request_body_size)
    data = parse_qs(request_body)

    # wsgi.input is a file-like object, so we need to decode it
    # urrlib.parse.parse_qs returns a dict with byte strings as values
    data = {k.decode(): [v.decode() for v in vals] for k, vals in data.items()}
    return data
