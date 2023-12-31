class Response:
    """
    TODO:
    - set default headers
    - handle different types of response bodies (eg. JSON, encode string as bytes).
    - set cookies (Set-Cookie header)
    - handle redirects (Location header), 302 status code
    - handle errors, 404, 500, etc.
    """

    def __init__(self, headers, status_code, response_body):
        self.response_body = response_body
        self.headers = headers
        self.status_code = status_code

    def __call__(self, environ, start_response):
        start_response(self.status_code, self.headers)
        return [self.response_body.encode("utf-8")]
