import json
from typing import Callable
from dataclasses import dataclass
from urllib.parse import parse_qs
from simple_http import constants


@dataclass
class Route:
    path: str
    method: str
    handler: Callable


class Request:
    def __init__(self, environ):
        self.environ = environ

    @property
    def path(self):
        return self.environ["PATH_INFO"]

    @property
    def method(self):
        return self.environ["REQUEST_METHOD"]

    @property
    def query_string(self):
        return parse_qs(self.environ.get("QUERY_STRING", ""))

    @property
    def post_body(self):
        return self.handle_body_data(self.environ)

    def handle_body_data(self, environ):
        # Temporary solution, we'll see how to handle this better later.
        try:
            request_body_size = int(environ.get("CONTENT_LENGTH", 0))
        except ValueError:
            request_body_size = 0

        input = environ["wsgi.input"]
        request_body = input.read(request_body_size)

        content_type = environ.get("CONTENT_TYPE", "")
        if content_type == "application/json":
            return json.loads(request_body)

        data = parse_qs(request_body)

        # wsgi.input is a file-like object, so we need to decode it
        # urrlib.parse.parse_qs returns a dict with byte strings as values
        return {k.decode(): [v.decode() for v in vals] for k, vals in data.items()}


class Response:
    def __init__(self, body, status, headers=None):
        self.body = body
        self.status = status
        self.headers = headers or [("Content-type", "text/plain")]


class Router:
    def __init__(self):
        self.routes = []

    def add_route(self, path, method="GET"):
        def decorator(func):
            self.routes.append(Route(path, method, func))
            return func

        return decorator

    def find_route(self, request):
        return next(
            (route for route in self.routes if route.path == request.path), None
        )


class MiddlewareManager:
    def __init__(self):
        self.middleware = []

    def register_middleware(self, middleware_func):
        self.middleware.append(middleware_func)

    def apply_middleware(self, request):
        for middleware_func in self.middleware:
            middleware_func(request)


class BasicWSGIServer:
    def __init__(self):
        self.router = Router()
        self.middleware_manager = MiddlewareManager()

    def route(self, path, method="GET"):
        return self.router.add_route(path, method)

    def use_middleware(self, request):
        self.middleware_manager.apply_middleware(request)

    def get_response_data(self, request):
        route = self.router.find_route(request)

        if not route:
            return Response("Not Found", constants.status_code_404)

        if request.method != route.method:
            return Response("Method Not Allowed", constants.status_code_405)

        response_body = route.handler(request)
        status = (
            constants.status_code_201
            if route.method == "POST"
            else constants.status_code_200
        )

        return Response(response_body, status)

    def __call__(self, environ, start_response):
        request = Request(environ)
        self.use_middleware(request)
        response = self.get_response_data(request)
        start_response(response.status, response.headers)
        return [response.body.encode("utf-8")]
