import re

import pytest
import requests
import json

from tests.request_templates.GeoInfoDataTemplate import GeoInfoDataTemplate


class TestGetComparison:
    keys = 'Geo_1', 'Geo_2'

    @pytest.mark.parametrize('keys', [(keys)])
    def test_hintname_200(self, keys):
        response = requests.post('http://127.0.0.1:8000/api/getcomparison', json={
            keys[0]: 'Знаменка',
            keys[1]: 'Явидово'
        })

        assert response.headers['Content-Type'] == 'application/json'
        assert response.status_code == 200

        json_response = json.loads(response.content.decode())

        for key in keys:
            response_values = dict(json_response[key.lower()]).values()
            GeoInfoDataTemplate().check_template_matches(list(response_values))

        result = json_response['compares']
        result is None or re.match(r'[-]?[0-9]{1,2}\.*[0-9]{0,2}$|0|"Undefinded"',
                                   str(result['Timezones_difference'])) and \
        re.match(r'[-]?[0-9]{1,3}\.*[0-9]{0,5}$', str(result['Northern latitude'])) and \
        result['Northern geo'] != "" and result['Northern geo'] is not None

    @pytest.mark.parametrize('keys', [(keys)])
    def test_getcomparison_check_match_with_pattern(self, keys):
        response = requests.post('http://127.0.0.1:8000/api/getcomparison', json={
            keys[0]: "Знаменка",
            keys[1]: "Yвидово"
        })

        assert response.headers['Content-Type'] == 'text/plain; charset=utf-8'
        assert response.status_code == 400
        assert response.text == f'Incorrect request!\n{keys[0]}, {keys[1]} include incorrect symbols!'

    @pytest.mark.parametrize('keys', [(keys)])
    def test_getpage_keys_not_found(self, keys):
        response = requests.post('http://127.0.0.1:8000/api/getcomparison', json={
            keys[0]: "Знаменка"
        })

        assert response.headers['Content-Type'] == 'text/plain; charset=utf-8'
        assert response.status_code == 400
        assert response.text == f'Incorrect request!\nIt must be json with keys {keys[0]}, {keys[1]}!'

