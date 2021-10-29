import requests


class TestRequestHeader:

    def test_request_header(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_header")

        assert "x-secret-homework-header" in response.headers, "There is no secret header in response"

        actual_header_value = response.headers.get("x-secret-homework-header")
        expected_header_value = "Some secret value"

        assert actual_header_value == expected_header_value, \
            f"Actual header value: '{actual_header_value}' is not the same as expected header value: '{expected_header_value}'"
