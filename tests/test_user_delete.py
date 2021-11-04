from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserDelete(BaseCase):

    def create_new_user(self):
        user_data = self.prepare_registration_data()
        response = MyRequests.post("/user/", data=user_data)
        Assertions.assert_code_status(response, 200), "New user not created"
        Assertions.assert_json_has_key(response, "id"), "New user not created"
        return response, user_data

    def test_delete_user_admin(self):
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }
        login_response = MyRequests.post("/user/login", data=data)
        auth_sid = self.get_cookie(login_response, "auth_sid")
        token = self.get_header(login_response, "x-csrf-token")

        delete_response = MyRequests.delete(
            "/user/2",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        Assertions.assert_code_status(delete_response, 400)
        assert delete_response.content.decode("utf-8") == "Please, do not delete test users with ID 1, 2, 3, 4 or 5.", \
            f"Unexpected response content {delete_response.content}"

    def test_delete_just_created_user(self):
        # Create user
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

        # Delete user
        delete_response = MyRequests.delete(
            "/user/2",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        Assertions.assert_code_status(delete_response, 200)

        # Get user details
        get_response = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        Assertions.assert_code_status(get_response, 404)
        assert get_response.content.decode("utf-8") == "User not found", \
            f"Unexpected response content {get_response.content}"

    def test_delete_user_authorized_as_other_user(self):
        # Create first user
        first_user_response, first_user_data = self.create_new_user()
        first_user_id = self.get_json_value(first_user_response, "id")

        # Create second user
        second_user_response, second_user_data = self.create_new_user()
        second_user_email = second_user_data["email"]
        second_user_password = second_user_data["password"]

        # Login as second user
        login_data = {
            "email": second_user_email,
            "password": second_user_password
        }
        login_response = MyRequests.post("/user/login", data=login_data)
        second_user_auth_sid = self.get_cookie(login_response, "auth_sid")
        second_user_token = self.get_header(login_response, "x-csrf-token")

        # Delete first user
        delete_response = MyRequests.delete(
            f"/user/{first_user_id}",
            headers={"x-csrf-token": second_user_token},
            cookies={"auth_sid": second_user_auth_sid}
        )
        Assertions.assert_code_status(delete_response, 200)

        # Get user details
        get_response = MyRequests.get(
            f"/user/{first_user_id}",
            headers={"x-csrf-token": second_user_token},
            cookies={"auth_sid": second_user_auth_sid}
        )
        # Verify user not deleted
        Assertions.assert_code_status(delete_response, 200)
        Assertions.assert_json_has_key(get_response, "username")
