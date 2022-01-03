from config.base_case import BaseCase
from config.assertions import Assertions
from config.my_requests import MyRequests
import time

class TestUserDelete(BaseCase):
    def test_delete_user_kotov(self):
        login_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response_login = MyRequests.post('user/login', data=login_data)
        token = self.get_header(response_login, 'x-csrf-token')
        auth_sid = self.get_cookie(response_login, 'auth_sid')
        user_id = self.get_json_value(response_login, 'user_id')
        Assertions.assert_code_status(response_login, 200)
        Assertions.assert_json_has_key(response_login, 'user_id')

        response_delete = MyRequests.delete(
            f'user/{user_id}',
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid}
            )
        Assertions.assert_code_status(response_delete, 400)
        assert response_delete.content.decode('utf-8') == f"Please, do not delete test users with ID 1, 2, 3, 4 or 5.", f'Successfully delete test user with ID 1, 2, 3, 4 or 5'

    def test_delete_just_created_user(self):
        data = self.prepare_registration_data()
        email = data['email']
        password = data['password']

        #Registration first user
        response_reg = MyRequests.post('user/', data=data)
        Assertions.assert_code_status(response_reg, 200)
        Assertions.assert_json_has_key(response_reg, 'id')

        data_login ={
            'email': email,
            'password': password
        }

        response_login = MyRequests.post('user/login', data=data_login)
        auth_sid = self.get_cookie(response_login, 'auth_sid')
        token = self.get_header(response_login, 'x-csrf-token')
        user_id = self.get_json_value(response_login, 'user_id')

        response_delete = MyRequests.delete(
            f'user/{user_id}',
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid}
            )

        Assertions.assert_code_status(response_delete, 200)

        response_get_deleted_user = MyRequests.get(
            f'user/{user_id}',
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid}
        )
        Assertions.assert_code_status(response_get_deleted_user, 404)
        assert response_get_deleted_user.content.decode('utf-8') == f"User not found", f'User {user_id} with {email} was not delete'

    def test_delete_another_user(self):
        data1 = self.prepare_registration_data()
        email1 = data1['email']
        password1 = data1['password']
        data_list = ['id', 'username', 'email', 'firstName', 'lastName']

        time.sleep(1)
        data2 = self.prepare_registration_data()
        email2 = data2['email']
        password2 = data2['password']

        #Registration first user
        response_reg1 = MyRequests.post('user/', data=data1)
        Assertions.assert_code_status(response_reg1, 200)
        Assertions.assert_json_has_key(response_reg1, 'id')

        #Registration second user
        response_reg2 = MyRequests.post('user/', data=data2)
        Assertions.assert_code_status(response_reg2, 200)
        Assertions.assert_json_has_key(response_reg2, 'id')

        data_login1 ={
            'email': email1,
            'password': password1
        }
        data_login2 ={
            'email': email2,
            'password': password2
        }

        #Login first user
        response_login1 = MyRequests.post('user/login', data=data_login1)
        auth_sid1 = self.get_cookie(response_login1, 'auth_sid')
        token1 = self.get_header(response_login1, 'x-csrf-token')
        user_id1 = self.get_json_value(response_login1, 'user_id')

        #Login second user
        response_login2 = MyRequests.post('user/login', data=data_login2)
        auth_sid2 = self.get_cookie(response_login2, 'auth_sid')
        token2 = self.get_header(response_login2, 'x-csrf-token')
        user_id2 = self.get_json_value(response_login2, 'user_id')

        #Delete second user by first user
        response_delete = MyRequests.delete(
            f'user/{user_id2}',
            headers={'x-csrf-token': token1},
            cookies={'auth_sid': auth_sid1}
            )
        Assertions.assert_code_status(response_delete, 200)

        response_get_second_user = MyRequests.get(
            f'user/{user_id2}',
            headers={'x-csrf-token': token2},
            cookies={'auth_sid': auth_sid2}
        )
        Assertions.assert_code_status(response_get_second_user, 200)
        Assertions.assert_json_has_keys(response_get_second_user, data_list)

