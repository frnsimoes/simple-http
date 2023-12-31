from simple_framework import BasicWSGIServer


app = BasicWSGIServer()


@app.route("/")
def home(environ):
    return "Welcome to the home page!"


@app.route("/about")
def about(environ):
    return "This is the about page."


def logging_middleware(environ):
    print(f"Request received for: {environ['PATH_INFO']}")


app.register_middleware(logging_middleware)
