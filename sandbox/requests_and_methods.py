import requests

url = "https://playground.learnqa.ru/ajax/api/compare_query_type"

# 1 Response: Wrong method provided, status code: 200
response = requests.get(url=url)
print(response.status_code, response.text, sep=", ")

# 2 Response: No response, status code: 400 Client error
response = requests.head(url=url)
print(response.status_code, response.text, sep=", ")

# 3 Response: {"success":"!"}, status code: 200
response = requests.post(url=url, data={"method": "POST"})
print(response.status_code, response.text, sep=", ")

# 4 Method DELETE with param GET returns success
methods = ["POST", "GET", "PUT", "DELETE"]
for method in methods:
    for params in methods:
        data = {"method": params}
        if method == "GET":
            response = requests.request(method, url=url, params=data)
            print(f"Method:{method} params:{str(data)} --> {response.text}")
        else:
            response = requests.request(method, url=url, data=data)
            print(f"Method:{method} params:{str(data)} --> {response.text}")