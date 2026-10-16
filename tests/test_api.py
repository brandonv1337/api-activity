import pytest

from api_activity.app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    with app.test_client() as client:
        yield client


def test_hello(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == {"message": "Hello World!"}


def test_square(client):
    response = client.get('/square/4')
    assert response.status_code == 200
    assert response.json == {'Shape': 'Square', 'Area': 16}


def test_echo(client):
    response = client.get('/echo?arg1=hello&arg2=world')
    assert response.status_code == 200
    assert response.json == {'arg1': 'hello', 'arg2': 'world'}


def test_cube_requires_auth(client):
    response = client.get('/cube/3')
    assert response.status_code == 401


def test_cube_rejects_wrong_password(client):
    client.put(
        '/register',
        json={"username": "testuser", "password": "testpass123"}
    )
    response = client.get('/cube/3', auth=("testuser", "wrongpassword"))
    assert response.status_code == 401


def test_cube_with_valid_auth(client):
    client.put(
        '/register',
        json={"username": "testuser", "password": "testpass123"}
    )
    response = client.get('/cube/3', auth=("testuser", "testpass123"))
    assert response.status_code == 200
    assert response.json == {'Shape': 'Cube', 'Volume': 27}