from simple_http import constants
from simple_http.dummy_db import DummyDB


def test_request_to_home(test_client):
    response = test_client.get("/")

    assert response.status == constants.status_code_200
    assert response.body == b"Welcome to the home page!"


def test_request_to_inexistent_route(test_client):
    response = test_client.get("/inexistent", expect_errors=True)

    assert response.status == constants.status_code_404
    assert response.body == b"Not Found"


def test_request_with_not_allowed_method(test_client):
    response = test_client.post("/", expect_errors=True)

    assert response.status == constants.status_code_405
    assert response.body == b"Method Not Allowed"


def test_body_create_user(test_client):
    DummyDB.clean()
    response = test_client.post("/create_user", params={"username": "test_user"})
    assert response.status == constants.status_code_201
    assert DummyDB.users == ["test_user"]
    assert response.body == b"test_user"


def test_query_string_create_user(test_client):
    DummyDB.clean()
    response = test_client.post("/create_user_with_qs?username=test_user")
    assert response.status == constants.status_code_201
    assert DummyDB.users == ["test_user"]
    assert response.body == b"test_user"
