import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect")
num_of_redirects = len(response.history)
print(num_of_redirects)
print(response.url)