from api_activity.app import create_app
import pytest
@pytest.fixture
def client():
    with create_app().test_client() as client:
        yield client

def test_hello():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == {'message': "Hello World!"}

def test_square(num):
    response = client.get('/square/<int:num>')
    assert response.status_code == 200
    assert response.json == ({'Shape':__class__.__name__, 'Area':num*num})