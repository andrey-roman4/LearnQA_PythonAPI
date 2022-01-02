import requests
from datetime import datetime


def prepare_email(email=None):
    base_part = 'learnqa'
    domain = 'example.com'
    random_part = datetime.now().strftime('%m%d%Y%H%M%S')
    email = f'{base_part}{random_part}@{domain}'
    return email


#email = 'vinkotovexample.com'
email = prepare_email()
data = {
    'password': '123',
    'username': 'learnqa',
    'firstName': 'learnqa',
    'lastName': 'learnqa',
    'email': email
    }

value = 'username'
long_name = '1234567890' * 26
print(len(long_name))
data[value] = long_name
print(data[value])
response = requests.post('https://playground.learnqa.ru/api/user/', data=data)
print(email)
print(response.status_code)
print(response.text)
#print(response.content)
#print(response.json())
