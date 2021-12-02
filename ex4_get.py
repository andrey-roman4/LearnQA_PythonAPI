import requests

link = 'https://playground.learnqa.ru/api/get_text'
response = requests.get(link)
print(response.text)