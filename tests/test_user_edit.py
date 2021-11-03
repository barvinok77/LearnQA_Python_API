from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserEdit(BaseCase):

    def create_new_user(self):
        user_data = self.prepare_registration_data()
        response = MyRequests.post("/user/", data=user_data)
        Assertions.assert_code_status(response, 200), "New user not created"
        Assertions.assert_json_has_key(response, "id"), "New user not created"
        return response, user_data

    def test_edit_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data["email"]
        first_name  = register_data["firstName"]
        password = register_data["password"]
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            "email": email,
            "password": password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "Changed Name"

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )

    def test_edit_not_authorized_user(self):
        # Register
        create_response, user_data = self.create_new_user()
        user_id = self.get_json_value(create_response, "id")

        # Edit
        new_name = "Changed Name"

        edit_response = MyRequests.put(
            f"/user/{user_id}",
            data={"firstName": new_name}
        )
        Assertions.assert_code_status(edit_response, 400)
        assert edit_response.content.decode("utf-8") == "Auth token not supplied", \
            f"Unexpected response content {edit_response.content}"

    def test_edit_other_authorized_user(self):
        # Register first user
        first_user_response, user_data = self.create_new_user()
        # Get first user data
        first_user_id = self.get_json_value(first_user_response, "id")
        first_user_email = user_data["email"]
        first_user_password = user_data["password"]
        old_name = user_data["firstName"]

        # Register second user
        second_user_response, user_data = self.create_new_user()
        # Get second user data
        second_user_email = user_data["email"]
        second_user_password = user_data["password"]

        # Login as second user and get authorization details
        login_data = {
            "email": second_user_email,
            "password": second_user_password
        }
        login_response = MyRequests.post("/user/login", data=login_data)
        second_user_auth_sid = self.get_cookie(login_response, "auth_sid")
        second_user_token = self.get_header(login_response, "x-csrf-token")

        # Edit first user being authorized as second user
        new_name = "Changed Name"

        edit_response = MyRequests.put(
            f"/user/{first_user_id}",
            headers={"x-csrf-token": second_user_token},
            cookies={"auth_sid": second_user_auth_sid},
            data={"firstName": new_name}
        )
        Assertions.assert_code_status(edit_response, 200)

        # Login as first user and get authorization details
        login_data = {
            "email": first_user_email,
            "password": first_user_password
        }
        login_response = MyRequests.post("/user/login", data=login_data)
        first_user_auth_sid = self.get_cookie(login_response, "auth_sid")
        first_user_token = self.get_header(login_response, "x-csrf-token")

        # Get first user details
        get_response = MyRequests.get(
            f"/user/{first_user_id}",
            headers={"x-csrf-token": first_user_token},
            cookies={"auth_sid": first_user_auth_sid}
        )
        # Assert first name has not been changed
        Assertions.assert_json_value_by_name(
            get_response,
            "firstName",
            old_name,
            "User's first name shouldn't been changed but it did"
        )

    def test_edit_authorized_user_incorrect_email(self):
        # Register
        create_response, user_data = self.create_new_user()
        user_id = self.get_json_value(create_response, "id")
        user_email = user_data["email"]
        user_password = user_data["password"]

        # Login
        login_data = {
            "email": user_email,
            "password": user_password
        }
        login_response = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(login_response, "auth_sid")
        token = self.get_header(login_response, "x-csrf-token")

        # Edit user
        new_email = "learnqaexample.com"

        edit_response = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": new_email}
        )
        Assertions.assert_code_status(edit_response, 400)
        assert edit_response.content.decode("utf-8") == "Invalid email format", \
            f"Unexpected response content {edit_response.content}"

    def test_edit_authorized_user_short_firstname(self):
        # Register
        create_response, user_data = self.create_new_user()
        user_id = self.get_json_value(create_response, "id")
        user_email = user_data["email"]
        user_password = user_data["password"]

        # Login
        login_data = {
            "email": user_email,
            "password": user_password
        }
        login_response = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(login_response, "auth_sid")
        token = self.get_header(login_response, "x-csrf-token")

        # Edit user
        new_name = "a"

        edit_response = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )
        Assertions.assert_code_status(edit_response, 400)
        assert edit_response.content.decode("utf-8") == '{"error":"Too short value for field firstName"}',\
            f"Unexpected response content {edit_response.content}"
