from simple_http.dummy_db import DummyDB
from simple_http.simple_http import BasicWSGIServer
from urllib.parse import parse_qs

app = BasicWSGIServer()


@app.route("/", method="GET")
def home(environ):
    return "Welcome to the home page!"


@app.route("/about", method="GET")
def about(environ):
    return "This is the about page."


@app.route("/create_user", method="POST")
def create_user(environ):
    data = handle_body_data(environ)

    username = data.get("username", [""])[0]
    DummyDB.create_user(username)
    return username


def handle_body_data(environ):
    try:
        request_body_size = int(environ.get("CONTENT_LENGTH", 0))
    except ValueError:
        request_body_size = 0

    input = environ["wsgi.input"]
    import ipdb

    ipdb.set_trace()

    request_body = input.read(request_body_size)
    data = parse_qs(request_body)

    # wsgi.input is a file-like object, so we need to decode it
    # urrlib.parse.parse_qs returns a dict with byte strings as values
    data = {k.decode(): [v.decode() for v in vals] for k, vals in data.items()}
    return data


def logging_middleware(environ):
    print(f"Request received for: {environ['PATH_INFO']}")


app.register_middleware(logging_middleware)
