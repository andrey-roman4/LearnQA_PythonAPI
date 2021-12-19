import requests
import json

def test_header_method():
    hea_value = '!'
    print(f"Value of checked cookies method is: '{hea_value}'")
    response = requests.request('GET', 'https://playground.learnqa.ru/api/homework_header')
    assert response.status_code == 200, "Response status is not 200"
    try:
        response_as_dict = response.json()
    except json.JSONDecodeError:
        assert False, f"Response is not JSON format. Response text is '{response.text}'"
    header_key_value = (list(response_as_dict))[0]
    header_value = response_as_dict[header_key_value]
    assert header_value == hea_value, f"Header value is not '{hea_value}'"