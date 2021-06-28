import pytest
import requests
import json

from tests.request_templates.GeoInfoDataTemplate import GeoInfoDataTemplate


class TestGetPage:
    keys = 'Page', 'Items_value'

    @pytest.mark.parametrize('keys', [(keys)])
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
            GeoInfoDataTemplate().check_template_matches(list(response_values))

    @pytest.mark.parametrize('keys', [(keys)])
    def test_getpage_positive_int_expected(self, keys):
        response = requests.post('http://127.0.0.1:8000/api/getpage', json={
            keys[0]: -1,
            keys[1]: 2
        })

        assert response.headers['Content-Type'] == 'text/plain; charset=utf-8'
        assert response.status_code == 400
        assert response.text == 'Incorrect request!\nPage, Items_value must be positive int.'

    @pytest.mark.parametrize('keys', [(keys)])
    def test_getpage_keys_not_found(self, keys):
        response = requests.post('http://127.0.0.1:8000/api/getpage', json={
            keys[1]: 2
        })

        assert response.headers['Content-Type'] == 'text/plain; charset=utf-8'
        assert response.status_code == 400
        assert response.text == 'Incorrect request!\nIt must be json with keys Page, Items_value!'
