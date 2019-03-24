import pytest
import os
import connexion
from connexion import FlaskApi

flask_app = connexion.FlaskApp(__name__)
flask_app.add_api('swagger.yml')


@pytest.fixture(scope='module')
def client():
    with flask_app.app.test_client() as c:
        yield c


def test_pass_submit(client):
    """Test expected submission"""
    url = '/api/submit'
    response = client.post(url,data={"userId":"foo","email":"foo@bar.com","data":"test"}
    )
    assert response.status_code == 200
