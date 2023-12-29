from simple_framework import HttpResponseBody


def test_http_response_body_is_iterable():
    body = 'hello world'
    resp = HttpResponseBody(body)
    iter(resp)
