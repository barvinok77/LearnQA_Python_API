import pytest
import allure
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


@allure.epic("Test cases for new user registration")
class TestUserRegister(BaseCase):
    invalid_registration_data = ([
        {
            "username": "learnqa",
            "firstName": "learnqa",
            "lastName": "learnqa",
            "email": "learnqa@example.com"
        },
        {
            "password": "123",
            "firstName": "learnqa",
            "lastName": "learnqa",
            "email": "learnqa@example.com"
        },
        {
            "password": "123",
            "username": "learnqa",
            "lastName": "learnqa",
            "email": "learnqa@example.com"
        },
        {
            "password": "123",
            "username": "learnqa",
            "firstName": "learnqa",
            "email": "learnqa@example.com"
        },
        {
            "password": "123",
            "username": "learnqa",
            "firstName": "learnqa",
            "lastName": "learnqa",
        }
    ])

    @allure.testcase('test case link', 'Test case title')
    @allure.link('link to documentation')
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.testcase('test case link', 'Test case title')
    @allure.issue('issue link')
    def test_create_user_with_existing_email(self):
        email = "vinkotov@example.com"
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
            f"Unexpected response content {response.content}"

    def test_create_user_with_incorrect_email(self):
        email = "vinkotovexample.com"
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "Invalid email format", \
            f"Unexpected response content {response.content}"

    @pytest.mark.parametrize("data", invalid_registration_data)
    def test_create_user_with_missing_fields(self, data):
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert "The following required params are missed:" in response.content.decode("utf-8"), \
            f"Unexpected response content {response.content}"

    def test_create_user_with_short_username(self):
        data = self.prepare_registration_data()
        data.update({"username": "a"})

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "The value of 'username' field is too short", \
            f"Unexpected response content {response.content}"

    def test_create_user_with_long_username(self):
        data = self.prepare_registration_data()
        data.update({"username": str("a" * 251)})

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "The value of 'username' field is too long", \
            f"Unexpected response content {response.content}"
