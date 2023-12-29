from simple_framework import BasicWSGIServer


def test_route_registration():
    app = BasicWSGIServer()

    @app.route("/test")
    def test_route(environ):
        return "Test"

    assert ("/test", test_route) in app.routes


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
    handler = app.handle_route(environ)

    assert handler == test_route


def test_response_headers_and_status():
    app = BasicWSGIServer()

    assert app.set_response_headers() == [("Content-type", "text/plain")]
    assert app.set_response_status() == "200 OK"


def test_call_return():
    app = BasicWSGIServer()

    @app.route("/test")
    def test_route(environ):
        return "Test"

    def dummy_start_response(status, headers):
        pass

    environ = {"PATH_INFO": "/test"}
    result = app(environ, dummy_start_response)
    assert result == [b"Test"]
