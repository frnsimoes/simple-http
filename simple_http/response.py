class Response:
    default_status = 200
    default_headers = [("Content-type", "text/plain")]
    """
    TODO:
    - set default headers
    - handle different types of response bodies (eg. JSON, encode string as bytes).
    - set cookies (Set-Cookie header)
    - handle redirects (Location header), 302 status code
    - handle errors, 404, 500, etc.
    """

    def __init__(self, headers, status_code, body):
        self.body = body
        self.headers = headers or self.default_headers
        self.status_code = status_code or self.default_status

    def __call__(self, environ, start_response):
        start_response(self.status_code, self.headers)
        return [self.body.encode("utf-8")]
