import json

json_text = '{"messages":[{"message":"This is the first message","timestamp":"2021-06-04 16:40:53"},{"message":"And this is a second message","timestamp":"2021-06-04 16:41:01"}]}'
json_obj = json.loads(json_text)

messages = "messages"
message = "message"

if messages in json_obj:
    if len(json_obj[messages]) > 1:
        if message in json_obj[messages][1]:
            print(json_obj[messages][1][message])
        else:
            print(f"Key {message} is not found in JSON")
    else:
        print("There is no second message in JSON")
else:
    print("There are no messages in JSON")