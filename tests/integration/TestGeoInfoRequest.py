import json
import pytest
import requests

from tests.response_templates.GeoInfoDataTemplate import GeoInfoDataTemplate
from config import request_keys


class TestGeoInfoRequest:
    @pytest.mark.parametrize('key', [(*request_keys['geoinfo'])])
    def test_getinfo_200(self, key):
        response = requests.post('http://127.0.0.1:8000/api/getinfo',
                                 json={
                                     key: 451750
                                 })

        assert response.headers['Content-Type'] == 'application/json'
        assert response.status_code == 200

        json_response = json.loads(response.content.decode())
        response_values = dict(json_response).values()

        GeoInfoDataTemplate().check_template_matches(list(response_values))

    @pytest.mark.parametrize('key', [(*request_keys['geoinfo'])])
    def test_getinfo_positive_int_expected(self, key):
        response = requests.post('http://127.0.0.1:8000/api/getinfo', json={
            key: -451750
        })

        assert response.headers['Content-Type'] == 'text/plain; charset=utf-8'
        assert response.status_code == 400
        assert response.text == f'Incorrect request!\n{key} must be positive int.'

    @pytest.mark.parametrize('key', [(*request_keys['geoinfo'])])
    def test_getinfo_keys_not_found(self, key):
        response = requests.post('http://127.0.0.1:8000/api/getinfo', json={
            'Geo': 451750
        })

        assert response.headers['Content-Type'] == 'text/plain; charset=utf-8'
        assert response.status_code == 400
        assert response.text == f'Incorrect request!\nIt must be json with keys {key}!'

    @pytest.mark.parametrize('key', [(*request_keys['geoinfo'])])
    def test_getinfo_geonameid_does_not_exist(self, key):
        response = requests.post('http://127.0.0.1:8000/api/getinfo', json={
            key: 1
        })

        assert response.headers['Content-Type'] == 'text/plain; charset=utf-8'
        assert response.status_code == 404
        assert response.text == 'Such geonameid does not exist!'
