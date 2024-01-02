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
def create_user_with_body(environ):
    data = environ['post_body']
    username = data.get("username", [""])[0]
    DummyDB.create_user(username)
    return username

@app.route("/create_user_with_qs", method="POST")
def create_user_with_qs(environ):
    data = environ['query_string']
    username = data.get("username", [""])[0]
    DummyDB.create_user(username)
    return username


def logging_middleware(environ):
    print(f"Request received for: {environ['PATH_INFO']}")


app.register_middleware(logging_middleware)
