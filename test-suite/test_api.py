import pytest
import connexion
from connexion import FlaskApi

flask_app = connexion.FlaskApp(__name__)
flask_app.add_api('../hook_system/processor/swagger.yml')


@pytest.fixture(scope='module')
def client():
    with flask_app.app.test_client() as c:
        yield c


def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
