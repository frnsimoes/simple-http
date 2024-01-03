from simple_http.request import Request
import io


def test_path():
    environ = {"PATH_INFO": "/test"}
    request = Request(environ)
    assert request.path == "/test"


def test_method():
    environ = {"REQUEST_METHOD": "GET"}
    request = Request(environ)
    assert request.method == "GET"


def test_query_string():
    environ = {"QUERY_STRING": "key=value"}
    request = Request(environ)
    assert request.query_string == {"key": ["value"]}


def test_post_body_json():
    environ = {
        "CONTENT_LENGTH": "17",
        "CONTENT_TYPE": "application/json",
        "wsgi.input": io.BytesIO(b'{"key": "value"}'),
    }
    request = Request(environ)
    assert request.post_body == {"key": "value"}


def test_post_body_form():
    environ = {
        "CONTENT_LENGTH": "9",
        "CONTENT_TYPE": "application/x-www-form-urlencoded",
        "wsgi.input": io.BytesIO(b"key=value"),
    }
    request = Request(environ)
    assert request.post_body == {"key": ["value"]}


def test_handle_body_data_invalid_content_length():
    environ = {
        "CONTENT_LENGTH": "invalid",
        "wsgi.input": io.BytesIO(b""),
    }
    request = Request(environ)
    assert request.handle_body_data(environ) == {}
