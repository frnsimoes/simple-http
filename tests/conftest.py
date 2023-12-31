import pytest
from webtest import TestApp

class TestClient:
    def __init__(self, application):
        self.app = TestApp(application)

    def get(self, path):
        response = self.app.get(path)
        return self._format_response(response)

    def request(self, method, path, data=None):
        response = self.app.request(path, method=method, params=data)
        return self._format_response(response)

    def _format_response(self, response):
        return {
            "status": response.status,
            "headers": response.headers,
            "body": response.text,
        }


@pytest.fixture(autouse=True)
def test_client():
    from app import app

    return TestClient(app)
