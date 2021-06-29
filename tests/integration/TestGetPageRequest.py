import pytest
import requests
import json

from response_templates.GeoInfoDataTemplate import GeoInfoDataTemplate
from config import request_keys


class TestGetPage:
    @pytest.mark.parametrize('keys', [(request_keys['getpage'])])
    def test_getpage_200(self, keys):
        response = requests.post('http://127.0.0.1:8000/api/getpage', json={
            keys[0]: 1,
            keys[1]: 2
        })

        assert response.headers['Content-Type'] == 'application/json'
        assert response.status_code == 200

        json_response = json.loads(response.content.decode())

        assert len(json_response) == 2

        for item in json_response:
            response_values = dict(item).values()
            assert GeoInfoDataTemplate().check_template_matches(list(response_values))==True

    @pytest.mark.parametrize('keys', [(request_keys['getpage'])])
    def test_getpage_positive_int_expected(self, keys):
        response = requests.post('http://127.0.0.1:8000/api/getpage', json={
            keys[0]: -1,
            keys[1]: 2
        })

        assert response.headers['Content-Type'] == 'text/plain; charset=utf-8'
        assert response.status_code == 400
        assert response.text == f'Incorrect request!\n{keys[0]}, {keys[1]} must be positive int.'

    @pytest.mark.parametrize('keys', [(request_keys['getpage'])])
    def test_getpage_keys_not_found(self, keys):
        response = requests.post('http://127.0.0.1:8000/api/getpage', json={
            keys[1]: 2
        })

        assert response.headers['Content-Type'] == 'text/plain; charset=utf-8'
        assert response.status_code == 400
        assert response.text == f'Incorrect request!\nIt must be json with keys {keys[0]}, {keys[1]}!'
