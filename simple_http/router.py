from dataclasses import dataclass
from typing import Callable


@dataclass
class Route:
    path: str
    method: str
    handler: Callable


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
