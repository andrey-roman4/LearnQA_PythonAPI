import requests

response = requests.get('https://playground.learnqa.ru/api/long_redirect')
response_history = response.history
number_of_redirects = len(response_history)
last_url = response_history[-1].url
print(number_of_redirects)
print(last_url)