class Response:
    def __init__(self, body, status, headers=None):
        self.body = body
        self.status = status
        self.headers = headers or [("Content-type", "application/json")]
