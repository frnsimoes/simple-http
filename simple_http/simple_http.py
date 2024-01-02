from simple_http import constants
from simple_http.request import Request
from simple_http.response import Response
from simple_http.router import Router


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
