import requests
import pytest


request_params = [
    ({'User-Agent': 'Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'}, {'platform': 'Mobile', 'browser': 'No', 'device': 'Android'}),
    ({'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1'}, {'platform': 'Mobile', 'browser': 'Chrome', 'device': 'iOS'}),
    ({'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}, {'platform': 'Googlebot', 'browser': 'Unknown', 'device': 'Unknown'}),
    ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0'}, {'platform': 'Web', 'browser': 'Chrome', 'device': 'No'}),
    ({'User-Agent': 'Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'}, {'platform': 'Mobile', 'browser': 'No', 'device': 'iPhone'})
    ]

@pytest.mark.parametrize('user, expected', request_params)
def test_user_agent_check(user, expected):
    response = requests.request('GET', 'https://playground.learnqa.ru/ajax/api/user_agent_check', headers=user)
    pl_fact_value = response.json()['platform']
    br_fact_value = response.json()['browser']
    dev_fact_value = response.json()['device']
    print(user)
    assert expected['platform'] == pl_fact_value, f'Platform is not equal. Ex - {expected["platform"]} / Fac - {pl_fact_value}'
    assert expected['browser'] == br_fact_value, f'Browser is not equal. Ex - {expected["browser"]} / Fac - {br_fact_value}'
    assert expected['device'] == dev_fact_value, f'Device is not equal. Ex - {expected["device"]} / Fac - {dev_fact_value}'
