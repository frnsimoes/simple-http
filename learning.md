30/12/2023 17:52:07
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
