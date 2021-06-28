from typing import List

import pytest
import requests
import json


class TestHintName:
    key = 'Hint'

    @pytest.mark.parametrize('key', [(key)])
    def test_hintname_200(self, key):
        response = requests.post('http://127.0.0.1:8000/api/hintname', json={
            key: 'Yasnaya'
        })

        assert response.headers['Content-Type'] == 'application/json'
        assert response.status_code == 200

        json_response = json.loads(response.content.decode())

        assert isinstance(json_response, List)

    @pytest.mark.parametrize('key', [(key)])
    def test_getcomparison_check_match_with_pattern(self, key):
        response = requests.post('http://127.0.0.1:8000/api/hintname', json={
            key: 'Yasnaya!'
        })

        assert response.headers['Content-Type'] == 'text/plain; charset=utf-8'
        assert response.status_code == 400
        assert response.text == f'Incorrect request!\n{key} include incorrect symbols!'

    @pytest.mark.parametrize('key', [(key)])
    def test_getpage_keys_not_found(self, key):
        response = requests.post('http://127.0.0.1:8000/api/hintname', json={
            'Hnt': "Знаменка"
        })

        assert response.headers['Content-Type'] == 'text/plain; charset=utf-8'
        assert response.status_code == 400
        assert response.text == f'Incorrect request!\nIt must be json with keys {key}!'