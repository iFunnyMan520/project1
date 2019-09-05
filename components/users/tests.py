import datetime
import os
import pytest

from server import get_app, config
from components.users.models import User, UserConfirmationToken, \
    UserSessionToken


@pytest.fixture(scope='session', autouse=True)
def server():
    if os.path.exists(config.DB_PATH):
        os.remove(config.DB_PATH)

    new_instance = get_app()

    with new_instance.app_context():
        config.db.create_all()

    return new_instance


@pytest.fixture(scope='session')
def client(server):
    return server.test_client(use_cookies=True)


def test_not_allowed_methods(client):
    response = client.get('/api/v1/user/login/')
    assert response.status_code == 405

    response = client.get('/api/v1/user/confirm/')
    assert response.status_code == 405


def test_login_process(server, client):
    response = client.post('/api/v1/user/login/',
                           json=dict(phone='phone'))
    assert response.status_code == 200
    assert response.data == b'Sms was sent'

    with server.app_context():
        token: UserConfirmationToken = UserConfirmationToken.query\
            .join(User).filter(User.phone == 'phone')\
            .first()

    data = dict(phone='phone', token=token.token)
    response = client.post('/api/v1/user/confirm/', json=data)

    user_id = response.json.get('id')
    assert response.status_code == 200
    assert user_id == token.user_id

    response = client.get('/api/v1/me/')
    assert response.json.get('id') == user_id

    with server.app_context():
        session: UserSessionToken = UserSessionToken.query\
            .filter(UserSessionToken.user_id == user_id)\
            .first()
        session.created_at += datetime.timedelta(days=365)
        config.db_session.commit()

    response = client.get('/api/v1/me/')
    assert response.status_code == 403

    with server.app_context():
        session.created_at += datetime.datetime.now()
        config.db_session.commit()

    response = client.get('/api/v1/logout/')
    assert response.status_code == 200
