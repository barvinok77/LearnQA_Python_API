import requests


class TestRequestCookie:

    def test_request_cookie(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_cookie")

        assert "HomeWork" in response.cookies, "There is no cookie in response"

        actual_cookie_value = response.cookies.get("HomeWork")
        expected_cookie_value = "hw_value"

        assert actual_cookie_value == expected_cookie_value, \
            f"Actual cookie value: '{actual_cookie_value}' is not the same as expected cookie value: '{expected_cookie_value}'"