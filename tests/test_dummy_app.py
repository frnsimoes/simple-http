def test_request_to_home(test_client):
    response = test_client.get("/")

    assert response["status"] == "200 OK"
    assert response["body"] == "Welcome to the home page!"


def test_request_to_inexistent_route(test_client):
    response = test_client.get("/inexistent")

    assert response["status"] == "200 OK"
    assert response["body"] == "Not Found"
