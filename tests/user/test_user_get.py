from config.my_requests import MyRequests
from config.base_case import BaseCase
from config.assertions import Assertions

class TestUserGet(BaseCase):
    def test_get_user_datails_not_auth(self):
        response = MyRequests.get('user/2')
        Assertions.assert_json_has_key(response, 'username')
        Assertions.assert_json_has_not_key(response, 'email')
        Assertions.assert_json_has_not_key(response, 'firstName')
        Assertions.assert_json_has_not_key(response, 'lastName')

    def test_user_datails_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post('user/login', data=data)
        auth_sid = self.get_cookie(response1, 'auth_sid')
        token = self.get_header(response1, 'x-csrf-token')
        user_id_from_auth_method = self.get_json_value(response1, 'user_id')

        response2 = MyRequests.get(
            f'user/{user_id_from_auth_method}',
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid}
            )
        
        expected_fields = ['username', 'email', 'firstName', 'lastName']
        Assertions.assert_json_has_keys(response2, expected_fields)
    
    def test_user_datails_as_other_user(self):
        data = {
            'email': 'learnqa01022022144823@example.com',
            'password': '123'
        }

        response1 = MyRequests.post('user/login', data=data)
        auth_sid = self.get_cookie(response1, 'auth_sid')
        token = self.get_header(response1, 'x-csrf-token')
        Assertions.assert_json_has_key(response1, 'user_id')
        user_id_from_auth_method = self.get_json_value(response1, 'user_id')

        response2 = MyRequests.get(
            f'user/{user_id_from_auth_method - 1}',
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid}
            )
        
        Assertions.assert_json_has_key(response2, 'username')
        Assertions.assert_json_has_not_key(response2, 'email')
        Assertions.assert_json_has_not_key(response2, 'firstName')
        Assertions.assert_json_has_not_key(response2, 'lastName')