import pytest
from webtest import TestApp


@pytest.fixture(autouse=True)
def test_client():
    from simple_http.dummy_app import app

    return TestApp(app)
