import pathlib
import tempfile
import unittest
import connexion


TEST_FOLDER = pathlib.Path(__file__).parent
print(TEST_FOLDER / "../hook_system/processor/Src/swagger.yml")


class TestAPI(unittest.TestCase):
    def setUp(self):
        flask_app = connexion.FlaskApp(__name__)
        flask_app.add_api(PATH_TO_YML)
        with flask_app.app.test_client() as c:
            yield c

    def test_submit(client):
        headers={'licence': '10293'}
        response = client.post('/submit', data=dict(
            userId='aaaa',
            email='a123@example.com',
            data=TEST_FOLDER+"/fake_data/test.tar.gz"),
            headers=headers)
        assert response.status_code == 200

    def test_results(client):
        response = client.post('/results', headers=headers,
            userId='aaaa',
            jobId='123'
            )
        assert response.status_code == 200
