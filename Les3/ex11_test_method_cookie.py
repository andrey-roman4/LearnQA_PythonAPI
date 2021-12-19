import requests

def test_cookies_method():
    coo_value = 'hw_value'
    print(f"Value of checked cookies method is: '{coo_value}'")
    response = requests.request('GET', 'https://playground.learnqa.ru/api/homework_cookie')
    assert response.status_code == 200, "Response status is not 200"
    assert dict(response.cookies), "There is no cookies in response"
    cookie_key_list = response.cookies.keys()
    cookie_value = response.cookies.get(cookie_key_list[0])
    assert cookie_value == coo_value, f"Cookie value is not '{coo_value}'"
