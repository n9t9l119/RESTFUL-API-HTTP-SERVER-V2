import requests


def test_getinfo():
    response = requests.post('http://127.0.0.1:8000/api/getinfo',json={
        "Geo_id": 451750
    })

    assert response.text == ('{"geonameid":451750,"name":"Zhitovo","asciiname":"Zhitovo","alternatenames":"",'
                             '"latitude":"57.29693","longitude":"34.41848","feature class":"P","feature_code":"PPL",'
                             '"country_code":"RU","cc2":"","admin1_code":"77","admin2_code":"","admin3_code":"",'
                             '"admin4_code":"","population":0,"elevation":"","dem":247,"timezone":"Europe/Moscow",'
                             '"modification_date":"2011-07-09"}\n')

def test_getpage():
    response = requests.post('http://127.0.0.1:8000/api/getpage', json={
        "Page": 1,
        "Items_value": 2
    })

    print(response.text)


def test_getcomparison():
    response = requests.post('http://127.0.0.1:8000/api/getcomparison', json={
        "Geo_1": "Знаменка",
        "Geo_2": "Явидово"
    })

    print(response.text)


def test_hintname():
    response = requests.post('http://127.0.0.1:8000/api/hintname', json={
        "Hint": 'Yasnaya'
    })

    print(response.text)
