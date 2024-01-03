from webtest import TestApp
from simple_http.simple_http import BasicWSGIServer


def test_get_route():
    server = BasicWSGIServer()
    server.route("/test", method="GET")(lambda req: "Hello, World!")

    app = TestApp(server)
    response = app.get("/test")

    assert response.status_code == 200
    assert response.text == "Hello, World!"


def test_post_route():
    server = BasicWSGIServer()
    server.route("/test", method="POST")(lambda req: "Hello, World!")

    app = TestApp(server)
    response = app.post("/test")

    assert response.status_code == 201
    assert response.text == "Hello, World!"


def test_not_found():
    server = BasicWSGIServer()

    app = TestApp(server)
    response = app.get("/test", expect_errors=True)

    assert response.status_code == 404


def test_method_not_allowed():
    server = BasicWSGIServer()
    server.route("/test", method="GET")(lambda req: "Hello, World!")

    app = TestApp(server)
    response = app.post("/test", expect_errors=True)

    assert response.status_code == 405
