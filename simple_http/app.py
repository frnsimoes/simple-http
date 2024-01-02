from simple_http.dummy_db import DummyDB
from simple_http.simple_http import BasicWSGIServer

app = BasicWSGIServer()


@app.route("/", method="GET")
def home(environ):
    return "Welcome to the home page!"


@app.route("/about", method="GET")
def about(environ):
    return "This is the about page."


@app.route("/create_user", method="POST")
def create_user_with_body(request):
    data = request.post_body
    username = data.get("username", [""])[0]
    DummyDB.create_user(username)
    return username


@app.route("/create_user_with_qs", method="POST")
def create_user_with_qs(request):
    data = request.query_string
    username = data.get("username", [""])[0]
    DummyDB.create_user(username)
    return username


@app.route("/create_user_with_json", method="POST")
def create_user_with_json(request):
    data = request.post_body
    username = data["username"]
    DummyDB.create_user(username)
    return username
