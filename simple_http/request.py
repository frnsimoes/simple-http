import json
from urllib.parse import parse_qs


class Request:
    def __init__(self, environ):
        self.environ = environ

    @property
    def path(self):
        return self.environ["PATH_INFO"]

    @property
    def method(self):
        return self.environ["REQUEST_METHOD"]

    @property
    def query_string(self):
        return parse_qs(self.environ.get("QUERY_STRING", ""))

    @property
    def post_body(self):
        return self.handle_body_data(self.environ)

    def handle_body_data(self, environ):
        # Temporary solution, we'll see how to handle this better later.
        try:
            request_body_size = int(environ.get("CONTENT_LENGTH", 0))
        except ValueError:
            request_body_size = 0

        input = environ["wsgi.input"]
        request_body = input.read(request_body_size)

        content_type = environ.get("CONTENT_TYPE", "")
        if content_type == "application/json":
            return json.loads(request_body)

        data = parse_qs(request_body)

        # wsgi.input is a file-like object, so we need to decode it
        # urrlib.parse.parse_qs returns a dict with byte strings as values
        return {k.decode(): [v.decode() for v in vals] for k, vals in data.items()}
