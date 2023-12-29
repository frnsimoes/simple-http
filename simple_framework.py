class BasicWSGIServer:
    def __init__(self):
        self.routes = []
        self.middleware = []

    def route(self, path):
        def decorator(func):
            self.routes.append((path, func))
            return func

        return decorator

    def register_middleware(self, middleware_func):
        self.middleware.append(middleware_func)

    def use_middleware(self, environ):
        for middleware_func in self.middleware:
            middleware_func(environ)

    def handle_route(self, environ):
        # Find the appropriate route
        path = environ["PATH_INFO"]
        return next(
            (handler for route_path, handler in self.routes if route_path == path), None
        )

    def set_response_headers(self):
        return [("Content-type", "text/plain")]

    def set_response_status(self):
        return "200 OK"

    def __call__(self, environ, start_response):
        self.use_middleware(environ)

        route_handler = self.handle_route(environ)
        if route_handler is not None:
            response_body = route_handler(environ)
        else:
            response_body = b"Not Found"

        status, headers = self.set_response_status(), self.set_response_headers()
        response = Response(headers, status, response_body)
        return response(environ, start_response)

class HttpResponseBody:
    def __init__(self, response_body):
        self.response_body = response_body

    def __iter__(self):
        yield self.response_body.encode("utf-8")

class Response:
    """
    TODO:
    - set default headers
    - handle different types of response bodies (eg. JSON, encode string as bytes).
    - set cookies (Set-Cookie header)
    - handle redirects (Location header), 302 status code
    - handle errors, 404, 500, etc.
    """
    def __init__(self, headers, status_code, response_body):
        self.response_body = response_body
        self.headers = headers
        self.status_code = status_code

    def __call__(self, environ, start_response):
        start_response(self.status_code, self.headers)
        return HttpResponseBody(self.response_body)
