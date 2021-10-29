import json.decoder
import requests
import pytest


class TestUserAgent:

    user_agent = [{"header": "Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) "
                             "AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
                   "platform": "Mobile", "browser": "No", "device": "Android"},
                  {"header": "Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) "
                             "CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1",
                   "platform": "Mobile", "browser": "Chrome", "device": "iOS"},
                  {"header": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
                   "platform": "Googlebot", "browser": "Unknown", "device": "Unknown"},
                  {"header": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0",
                   "platform": "Web", "browser": "Chrome", "device": "No"},
                  {"header": "Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 "
                             "(KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
                   "platform": "Mobile", "browser": "No", "device": "iPhone"}]

    @pytest.mark.parametrize("user_agent", user_agent)
    def test_user_agent(self, user_agent):

        url = "https://playground.learnqa.ru/ajax/api/user_agent_check"
        headers = {"User-Agent": user_agent["header"]}

        response = requests.get(url, headers=headers)
        try:
            dict_response = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not in JSON Format. Response text is '{response.text}'"

        assert dict_response["platform"] == user_agent["platform"], \
        f"Actual platform: '{dict_response['platform']}' is not the same as expected platform: '{user_agent['platform']}'"
        assert dict_response["browser"] == user_agent["browser"], \
        f"Actual browser: '{dict_response['browser']}' is not the same as expected browser: '{user_agent['browser']}'"
        assert dict_response["device"] == user_agent["device"], \
        f"Actual device: '{dict_response['device']}' is not the same as expected device: '{user_agent['device']}'"
