from config.my_requests import MyRequests
from config.base_case import BaseCase
from config.assertions import Assertions
import pytest

class TestUserRegister(BaseCase):
    missing_params = [
        ('password'),
        ('username'),
        ('firstName'),
        ('lastName')
    ]

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post('user/', data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, 'id')

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)
        response = MyRequests.post('user/', data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode('utf-8') == f"Users with email '{email}' already exists", f'Unexpected response content {response.content}'
    
    def test_create_user_without_symbol_bog_email(self):
        email = 'vinkotovexample.com'
        data = self.prepare_registration_data(email)
        response = MyRequests.post('user/', data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode('utf-8') == f"Invalid email format", f'Unexpected response content {response.content}'

    @pytest.mark.parametrize('value', missing_params)
    def test_create_user_without_one_value(self, value):
        email = 'vinkotov@example.com'
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
            }
        data[value] = ''

        response = MyRequests.post('user/', data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode('utf-8') == f"The value of '{value}' field is too short", f'Successful authorization without a required parameter {value}'

    def test_create_user_with_short_username(self):
        data = self.prepare_registration_data()
        data['username'] = 'a'

        response = MyRequests.post('user/', data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode('utf-8') == f"The value of 'username' field is too short", f'Successful authorization with short username'

    def test_create_user_with_long_username(self):
        data = self.prepare_registration_data()
        data['username'] = '1234567890' * 26

        response = MyRequests.post('user/', data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode('utf-8') == f"The value of 'username' field is too long", f'Successful authorization with long username'
      
