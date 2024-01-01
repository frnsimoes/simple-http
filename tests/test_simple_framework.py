from simple_http.simple_http import BasicWSGIServer, Route


def test_route_registration():
    app = BasicWSGIServer()

    @app.route("/test")
    def test_route(environ):
        return "Test"

    assert Route("/test", "GET", test_route) in app.routes


def test_route_registration_with_method():
    app = BasicWSGIServer()

    @app.route("/test", method="POST")
    def test_route(environ):
        return "Test"

    assert Route("/test", "POST", test_route) in app.routes


def test_middleware_registration():
    app = BasicWSGIServer()

    def test_middleware(environ):
        environ["test"] = "Test"

    app.register_middleware(test_middleware)

    assert test_middleware in app.middleware


def test_middleware_application():
    app = BasicWSGIServer()
    environ = {}

    def test_middleware(environ):
        environ["test"] = "test middleware applied"

    app.register_middleware(test_middleware)
    app.use_middleware(environ)

    assert environ["test"] == "test middleware applied"


def test_route_handling():
    app = BasicWSGIServer()

    @app.route("/test")
    def test_route(environ):
        return "Test"

    environ = {"PATH_INFO": "/test"}
    route = app.get_route(environ)

    assert route == Route("/test", "GET", test_route)


def test_call_return():
    app = BasicWSGIServer()

    @app.route("/test")
    def test_route(environ):
        return "Test"

    def dummy_start_response(status, headers):
        pass

    environ = {"PATH_INFO": "/test", "REQUEST_METHOD": "GET"}
    result = app(environ, dummy_start_response)
    assert result == [b"Test"]
