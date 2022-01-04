from config.my_requests import MyRequests
from config.base_case import BaseCase
from config.assertions import Assertions
import pytest
import allure

@allure.epic('User registration')
class TestUserRegister(BaseCase):
    missing_params = [
        ('password'),
        ('username'),
        ('firstName'),
        ('lastName')
    ]

    @allure.title("Successfully registration user")
    @allure.description("This test checking successfully registration user")
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post('user/', data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, 'id')

    @allure.title("Registration user with existing email")
    @allure.description("This test checking registration user with existing email")
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)
        response = MyRequests.post('user/', data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode('utf-8') == f"Users with email '{email}' already exists", f'Unexpected response content {response.content}'
    
    @allure.title("Registration user without symbol '@' in email")
    @allure.description("This test checking registration user without symbol '@' in his email")
    def test_create_user_without_symbol_bog_email(self):
        email = 'vinkotovexample.com'
        data = self.prepare_registration_data(email)
        response = MyRequests.post('user/', data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode('utf-8') == f"Invalid email format", f'Unexpected response content {response.content}'

    @allure.title("Registration user without one of required value")
    @allure.description("This test checking registration user without one of required value")
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

    @allure.title("Registration user with shot user name")
    @allure.description("This test checking registration user with shot user name")
    def test_create_user_with_short_username(self):
        data = self.prepare_registration_data()
        data['username'] = 'a'

        response = MyRequests.post('user/', data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode('utf-8') == f"The value of 'username' field is too short", f'Successful authorization with short username'

    @allure.title("Registration user with long user name")
    @allure.description("This test checking registration user with long user name")
    def test_create_user_with_long_username(self):
        data = self.prepare_registration_data()
        data['username'] = '1234567890' * 26

        response = MyRequests.post('user/', data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode('utf-8') == f"The value of 'username' field is too long", f'Successful authorization with long username'
      
