import requests
import time

url = "https://playground.learnqa.ru/ajax/api/longtime_job"

# create new task
response_1 = requests.get(url=url)

# get token and waiting time
json_1 = response_1.json()
token = json_1["token"]
seconds = json_1["seconds"]
params = {"token": token}

# verify unfinished task
response_2 = requests.get(url=url, params=params)
json_2 = response_2.json()

if json_2["status"] is not None:
    if json_2["status"] == "Job is NOT ready":
        print("Correct status")
    else:
        print("Wrong status")
else:
    print("No status - incorrect response")

# verify finished task
time.sleep(seconds)
response_3 = requests.get(url=url, params=params)
json_3 = response_3.json()

if json_3["status"] is not None:
    if json_3["status"] == "Job is ready" and json_3["result"] is not None:
        print("Correct status")
    else:
        print("Wrong status")
else:
    print("No status - incorrect response")