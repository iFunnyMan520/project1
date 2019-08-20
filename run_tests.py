import pytest

from server import app


@pytest.fixture(scope='session')
def client():
    return app.test_client()


def test_user_auth(client):
    expected_code = '12345'
    response = client.post(
        '/api/user/login/', data=dict(username='test_user'))
    assert response.data == expected_code.encode()

    response = client.post(
        '/api/user/login/confirm/', data=dict(code=expected_code))
    assert response.data == b'OK'
