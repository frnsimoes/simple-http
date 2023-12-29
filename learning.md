To create a web server, we need to implement the Web Server Gateway Interface (WSGI) standard. This is achieved through our BasicWSGIServer class.

In this class, we primarily work with two arguments: environ and start_response. The environ argument is a dictionary containing the CGI-style environment variables, which includes all the necessary HTTP request information. The start_response argument is a callback function supplied by the server which takes in two required positional arguments: status and response_headers.

We also built a simple server using Python's socket module. In this server, we first open a socket and bind it to an IP address and a port. We then set the server to listen for incoming connections. When a request is received, we accept it, which returns a new socket object representing the connection, and the address of the client.

We then use the start_response function to begin the HTTP response, and call our WSGI application (app) with environ and start_response as arguments. The application processes the request and returns the HTTP response body. We send this response back to the client, encoded as bytes, and then close the client socket, completing the HTTP request-response cycle.


## this I learned

- A especificação WSGI requer um iterável como retorno do response body. Isso permite enviar, de maneira mais eficiente, resposta maiores. Se o response body é grande, como, por exemplo, um arquivo, o server pode enviar para o client um pedaço por vez assim que ele é gerado, sem esperar que a geração da resposta inteira esteja pronta.

Isso é especialmente útil com conteúdos dinâmicos, onde o response body é gerado baseado na request. A aplicação pode começar a gerar o response body tão logo haja informação suficiente do primeiro pedaço (chunk).

A maneira que encontrei de fazer isso, sem utilizar forças um tipo iterável na string do response body, foi criando uma classe `Response` que é iterável.
