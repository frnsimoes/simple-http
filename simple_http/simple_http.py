from typing import Callable
from simple_http.response import Response
from simple_http import constants
from dataclasses import dataclass


@dataclass
class Route:
    path: str
    method: str
    handler: Callable

    # def __eq__(self, other):
    #     return self.path == other.path and self.method == other.method and self.handler == other.handler


class BasicWSGIServer:
    def __init__(self):
        self.routes = []
        self.middleware = []

    # def get_registered_paths(self):
    #     return [route.path for route in self.routes]

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

        for route in self.routes:
            if route.path == path:
                return route

    def method_allowed(self, environ):
        method = environ["REQUEST_METHOD"]
        """
        - check if method is in the list of allowed methods for the route
        - if not, return 405

        """
        route = self.get_route(environ)
        if not route:
            return False

        if method != route.method:
            return False

        return True

    def __call__(self, environ, start_response):
        self.use_middleware(environ)

        route = self.get_route(environ)
        if not route:
            response_body = "Not Found"
            status = constants.status_code_404

        elif not self.method_allowed(environ):
            response_body = "Method Not Allowed"
            status = constants.status_code_405

        else:
            response_body = route.handler(environ)
            if route.method == "POST":
                status = constants.status_code_201
            else:
                status = constants.status_code_200

        response = Response(headers=None, status_code=status, body=response_body)
        return response(environ, start_response)
