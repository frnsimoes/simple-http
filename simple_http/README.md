# Log de reflexões e aprendizados

## 30/12/2023
Minha primeira ideia era entender a implementação de um `web server` e de um `WSGI server`.

Percebi, contudo, que misturar as duas finalidades tornaria o estudo bastante complexo.

Responsabilidades do web server:
- Setup.
- Manipulação de connections.
- Parser de requests.
- Definição do ambiente WSGI, criando o conteúdo de `environ`.
- Criação do `start_response`.
- Parser de responses.
- Emissão da resposta para o Client.
- Fechamento da conexão.

Dessa forma, as únicas coisas que me parecem ser imediatas para o aprendizado são:

- Entender que `environ` e `start_response` são de responsabilidade do web server, e os utilizamos na aplicação WSGI apenas para utilização do web server (`environ`: dicionário que compartilha informações; `start_response`: call back function utilizada pelo web server).

- Focar no processamento da request e na geração do response body (objecto iterável).

...

Mudanças:
- Gunicorn adicionado como dependência.
- Webtest adicionado como dependência (acesso ao TestClient).
- Pytest adicionado.

## 31/12/2023
- Para ler o body de uma request, usa-se o `wsgi.input`, que é uma chave no dicionário `environ`. o input é um objeto file-like que fornce input do client para a aplicação. Uma vez que se lê o conteúdo, acessando o wsgi.input.read(), não é possível lê-lo novamente. Isso ocorre porque, em Python, quando se um arquivo é lido, a "posição" de leitura avança pelos bytes que já foram lidos. Os dados não são salvos em nenhum lugar depois de lidos.

- o CONTENT_LENGTH é bastante importante para evitar consumo excessivo de memória em arquivos muito grandes. Essa chave é utilizada para indicar o tamanho do body da request (no exemplo atual). Checar o integer máximo do CONTENT_LENGTH ajuda a não ler um arquivo gigantesco de uma vez só, o que beneficia o gerenciamento de memória, previne problemas com a segurança da aplicação e aumenta a eficiência (se a aplicação sabe o limite máximo do body, lhe é possível ler o body em chunks.)

Resumo:

- O Content-Length é um header HTTP que indica o tamanho do corpo da solicitação ou resposta em bytes.
- O corpo da solicitação é livro pelo `environ['wsgi.input].read()`. Passa-se o content-length como argumento do `read` por questões discutiadas acima.

## 01/01/2024
- Talvez eu tenha cometido um erro ao adicionar toda a lógica no `BasicWSGI`. Dessa forma, não consigo chamar o `Response` diretamente na view. A view retorna o body, e preciso manipular os headers e o status code dentro do `BasicWSGI`, o que me parece deselegante.

- O [werkzeug](https://github.com/pallets/werkzeug/blob/main/src/werkzeug/wrappers/response.py), de que o Flask faz uso, encapsula o app WSGI dentro do Response. Já o [Bottle](https://github.com/pallets/flask/blob/main/src/flask/app.py) cria o app WSGI dentro do próprio Bottle. Há apenas uma classe `HTTPResponse` que seta os headers, status_code, cookies, etc, mas nela não há nenhum comportamento.

Talvez a melhor solução momentânea seja deixar o BasicWSGI como o centro do qual emana o comportamento da aplicação, e abstrair o mínimo do Response (apenas o retorno de `body`, `status`, `headers`) e o Request (como encapsulador e replacer do `environ`). 
