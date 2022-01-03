from config.base_case import BaseCase
from config.assertions import Assertions
from config.my_requests import MyRequests

class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post('user/', data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, 'id')

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, 'id')

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post('user/login', data=login_data)

        auth_sid = self.get_cookie(response2, 'auth_sid')
        token = self.get_header(response2, 'x-csrf-token')

        # EDIT
        new_name = 'Change Name'

        response3 = MyRequests.put(
            f'user/{user_id}',
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid},
            data={'firstName': new_name}
            )

        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = MyRequests.get(
            f'user/{user_id}',
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid}
            )

        Assertions.assert_json_value_by_name(
            response4, 
            'firstName',
            new_name,
            'Wrong name of the user after edit'
        )

    def test_edit_unauthorized_user(self):
        new_name = 'Change-Name'
        response = MyRequests.put('user/21772', data={'firstName': new_name})
        Assertions.assert_code_status(response, 400)
        assert response.content.decode('utf-8') == f"Auth token not supplied", f'Successful change user name via unauthorized user'

    def test_edit_by_authorized_user_of_another_user(self):
        login_data_for_1 = {
            'email': 'learnqa01022022144823@example.com', # user_id = 21773
            'password': '123'
        }

        login_data_for_2 = {
            'email': 'learnqa01032022102421@example.com', # user_id = 21832
            'password': '123'
        }
        new_name = 'Change-Name'

        #Login first user
        response_from_login1user = MyRequests.post('user/login', data=login_data_for_1)

        auth_sid_for1 = self.get_cookie(response_from_login1user, 'auth_sid')
        token_for1 = self.get_header(response_from_login1user, 'x-csrf-token')
        user_id_from_auth_for1 = self.get_json_value(response_from_login1user, 'user_id')
        Assertions.assert_code_status(response_from_login1user, 200)
        Assertions.assert_json_has_key(response_from_login1user, 'user_id')

        #Login second user
        response_from_login2user = MyRequests.post('user/login', data=login_data_for_2)

        auth_sid_for2 = self.get_cookie(response_from_login2user, 'auth_sid')
        token_for2 = self.get_header(response_from_login2user, 'x-csrf-token')
        user_id_from_auth_for2 = self.get_json_value(response_from_login2user, 'user_id')
        Assertions.assert_code_status(response_from_login2user, 200)
        Assertions.assert_json_has_key(response_from_login2user, 'user_id')

        response_before_edit_user = MyRequests.get(
            f'user/{user_id_from_auth_for2}',
            headers={'x-csrf-token': token_for2},
            cookies={'auth_sid': auth_sid_for2}
        )
        username_before = (response_before_edit_user.json())['username']
        email_before = (response_before_edit_user.json())['email']
        firstname_before = (response_before_edit_user.json())['firstName']
        lastname_before = (response_before_edit_user.json())['lastName']

        response_for_edit_user2 = MyRequests.put(
            f'user/{user_id_from_auth_for2}',
            headers={'x-csrf-token': token_for1},
            cookies={'auth_sid': auth_sid_for1},
            data={'firstName': new_name}
            )
        
        response_after_edit_user = MyRequests.get(
            f'user/{user_id_from_auth_for2}',
            headers={'x-csrf-token': token_for2},
            cookies={'auth_sid': auth_sid_for2}
        )
        
        Assertions.assert_json_value_by_name(response_after_edit_user, 'username', username_before, f"User {user_id_from_auth_for2} has changed value of 'User Name'")
        Assertions.assert_json_value_by_name(response_after_edit_user, 'email', email_before, f"User {user_id_from_auth_for2} has changed value of 'Email'")
        Assertions.assert_json_value_by_name(response_after_edit_user, 'firstName', firstname_before, f"User {user_id_from_auth_for2} has changed value of 'First Name'")
        Assertions.assert_json_value_by_name(response_after_edit_user, 'lastName', lastname_before, f"User {user_id_from_auth_for2} has changed value of 'Last Name'")

    def test_edit_email_without_dog_symbol(self):
        data_for_login = {
            'password': '123',
            'email': 'learnqa01032022161132@example.com' # 21883
            }
        new_email = 'learnqa01032022161132example.com'

        response_from_login_user = MyRequests.post('user/login', data=data_for_login)
        token = self.get_header(response_from_login_user, 'x-csrf-token')
        auth_sid = self.get_cookie(response_from_login_user, 'auth_sid')
        user_id = self.get_json_value(response_from_login_user, 'user_id')
        Assertions.assert_code_status(response_from_login_user, 200)
        Assertions.assert_json_has_key(response_from_login_user, 'user_id')

        response_after_edit_wrong_email = MyRequests.put(
            f'user/{user_id}',
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid},
            data={'email': new_email}
            )
        Assertions.assert_code_status(response_after_edit_wrong_email, 400)
        assert response_after_edit_wrong_email.content.decode('utf-8') == f"Invalid email format", f'Successful change user email with broken email without symbol "@"'

    def test_edit_firstname_to_short_one(self):
        data_for_login = {
            'password': '123',
            'email': 'learnqa01032022161132@example.com' # 21883
            }
        new_firstname = 'a'

        response_from_login_user = MyRequests.post('user/login', data=data_for_login)
        token = self.get_header(response_from_login_user, 'x-csrf-token')
        auth_sid = self.get_cookie(response_from_login_user, 'auth_sid')
        user_id = self.get_json_value(response_from_login_user, 'user_id')
        Assertions.assert_code_status(response_from_login_user, 200)
        Assertions.assert_json_has_key(response_from_login_user, 'user_id')

        response_after_edit_short_firstname = MyRequests.put(
            f'user/{user_id}',
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid},
            data={'firstName': new_firstname}
            )
        Assertions.assert_code_status(response_after_edit_short_firstname, 400)
        assert response_after_edit_short_firstname.content.decode('utf-8') == '{"error":"Too short value for field firstName"}', f'Successful change User firstName with short firstName value'
