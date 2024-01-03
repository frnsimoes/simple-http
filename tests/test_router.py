from simple_http.request import Request
from simple_http.router import Route, Router

def test_route_creation():
    route = Route("/test", "GET", lambda req: "Hello, World!")
    assert route.path == "/test"
    assert route.method == "GET"
    assert route.handler({"path": "/test"}) == "Hello, World!"

def test_router_add_route():
    router = Router()

    @router.add_route("/test", method="GET")
    def handler(req):
        return "Hello, World!"

    route = router.routes[0]
    assert route.path == "/test"
    assert route.method == "GET"
    assert route.handler({"path": "/test"}) == "Hello, World!"

def test_router_find_route():
    router = Router()

    @router.add_route("/test", method="GET")
    def handler(req):
        return "Hello, World!"

    request = Request(environ={'PATH_INFO': '/test'})
    route = router.find_route(request)
    assert route is not None
    assert route.path == "/test"
    assert route.method == "GET"
    assert route.handler(request) == "Hello, World!"

def test_router_find_route_not_found():
    router = Router()
    request = Request(environ={'PATH_INFO': '/test'})
    route = router.find_route(request)
    assert route is None
