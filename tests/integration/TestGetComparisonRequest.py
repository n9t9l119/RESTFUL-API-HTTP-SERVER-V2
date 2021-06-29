import pytest
import requests
import json

from tests.response_templates.GeoInfoDataTemplate import GeoInfoDataTemplate
from config import request_keys
from tests.response_templates.GeoComparesDataTemplate import GeoComparesDataTemplate


class TestGetComparison:
    @pytest.mark.parametrize('keys', [(request_keys['getcomparison'])])
    def test_getcomparison_200(self, keys):
        response = requests.post('http://127.0.0.1:8000/api/getcomparison', json={
            keys[0]: 'Знаменка',
            keys[1]: 'Явидово'
        })

        assert response.headers['Content-Type'] == 'application/json'
        assert response.status_code == 200

        json_response = json.loads(response.content.decode())

        for key in keys:
            response_values = dict(json_response[key]).values()
            GeoInfoDataTemplate().check_template_matches(list(response_values))

        assert GeoComparesDataTemplate().check_template_matches(dict(json_response)['compares'])

    @pytest.mark.parametrize('keys', [(request_keys['getcomparison'])])
    def test_getcomparison_check_match_with_pattern(self, keys):
        response = requests.post('http://127.0.0.1:8000/api/getcomparison', json={
            keys[0]: "Знаменка",
            keys[1]: "Yвидово"
        })

        assert response.headers['Content-Type'] == 'text/plain; charset=utf-8'
        assert response.status_code == 400
        assert response.text == f'Incorrect request!\n{keys[0]}, {keys[1]} include incorrect symbols!'

    @pytest.mark.parametrize('keys', [(request_keys['getcomparison'])])
    def test_getcomparison_keys_not_found(self, keys):
        response = requests.post('http://127.0.0.1:8000/api/getcomparison', json={
            keys[0]: "Знаменка"
        })

        assert response.headers['Content-Type'] == 'text/plain; charset=utf-8'
        assert response.status_code == 400
        assert response.text == f'Incorrect request!\nIt must be json with keys {keys[0]}, {keys[1]}!'

