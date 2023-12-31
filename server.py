# import socket

# from simple_framework import BasicWSGIServer


# def get_request_data(client_socket: socket.socket):
#     request = client_socket.recv(1024).decode("utf-8")
#     request_line, headers_alone = request.split("\r\n", 1)
#     method, path, version = request_line.split(" ")

#     return method, path


# def start_server(app: BasicWSGIServer):
#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#     server_socket.bind(("127.0.0.1", 8000))
#     server_socket.listen(1)
#     print("Server started on http://127.0.0.1:8000")

#     while True:
#         client_socket, addr = server_socket.accept()
#         print("Received a connection from %s" % str(addr))
#         method, path = get_request_data(client_socket)

#         headers_set = []

#         def start_response(status, response_headers, exc_info=None):
#             headers_set[:] = [status, response_headers]

#         # Create the environ dict required by the WSGI spec
#         environ = {
#             "REQUEST_METHOD": method,
#             "PATH_INFO": path,
#             "SERVER_NAME": "127.0.0.1",
#             "SERVER_PORT": "8000",
#         }

#         # Call our framework
#         app_call = app(environ, start_response)

#         # Use the data returned by the app to create a response
#         response = get_response(headers_set, app_call)

#         # Send the response
#         client_socket.sendall(response.encode())
#         client_socket.close()


# def get_response(headers_set: list, app_call) -> str:
#     response = "HTTP/1.1 {0}\r\n".format(headers_set[0])
#     for header in headers_set[1]:
#         response += "{0}: {1}\r\n".format(*header)
#     response += "\r\n"
#     for data in app_call:
#         response += str(data)

#     return response
