import pytest

from app.main import create_app

TEST_NUMBER = "+11234567890"
TEST_BODY = "Test body response"


@pytest.fixture
def client():
    """Configures application for testing"""
    application = create_app()
    client = application.test_client()

    yield client


def test_sms_post(client):
    """Tests basic valid API functionality"""
    response = client.post("/sms", data=dict(From=TEST_NUMBER, Body=TEST_BODY))
    assert response.status_code == 200
