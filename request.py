# class Request:
#     def __init__(self, environ):
#         self.method = environ["REQUEST_METHOD"]
#         self.path = environ["PATH_INFO"]
#         self.headers = self.parse_headers(environ)
#         if self.method == "POST":
#             self.body = self.parse_body(environ)

#     def parse_headers(self, environ):
#         # Extract and parse headers from environ
#         pass

#     def parse_body(self, environ):
#         # Extract and parse body from environ
#         pass
