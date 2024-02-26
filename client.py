import requests

response = requests.post(
    "http://localhost:5000/user",
    json={
        "password": "1234fgwesge35235",
        "name": "user_5",
        "title": "asdasd",
        "description": "123123"
    },
)
print(response.text)
print(response.status_code)

# response = requests.get(
#     'http://localhost:5000/user/100',
# )
# print(response.text)
# print(response.status_code)


# response = requests.patch(
#     'http://localhost:5000/user/6',
#     json={"name": "user_1"}
# )
# print(response.text)
# print(response.status_code)

# response = requests.get(
#     'http://localhost:5000/user/1',
# )
# print(response.text)
# print(response.status_code)


# response = requests.delete(
#     'http://localhost:5000/user/6',
# )
# print(response.text)
# print(response.status_code)
