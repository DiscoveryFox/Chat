import json
from pprint import pprint

import requests

# api_key = requests.post("http://127.0.0.1:5000/auth", data={"id": "1", "password.txt": "test"}).text

# print(api_key)

with open('api_key', 'r') as file:
    api_key = file.read()

print(api_key)

# print(hashlib.blake2b(bytes("test", 'utf-8')).hexdigest())

contacts = requests.post("http://127.0.0.1:5000/get_contacts", data={"api_key": api_key,
                                                                     "sender": "1"}).text
contacts_json = json.loads(contacts)
# print(type(contacts_json)) -> list
print(contacts_json)

all_messages = requests.post("http://127.0.0.1:5000/get_all_messages", data={"api_key": api_key,
                                                                             "sender": "1"}).text
all_messages_json = json.loads(all_messages)
# print(type(messages_json))  # -> dict
# print(messages_json)

# pprint(messages_json)

# get all keys from dict


for contact in all_messages_json.keys():
    print(contact)
    for message in all_messages_json[contact]:
        print()
        print(message[1], end=' | ')
        print(message[2])
        print()

message = 'This is a message that was send by the API'

'''
feedback = requests.post('http://127.0.0.1:5000/send_message', data={"api_key": api_key,
                                                                     "sender": "1",
                                                                     "receiver": "8",
                                                                     "message": message})
                                                                     
'''

# print(feedback.text)

messages_from_1_to_8 = requests.post("http://127.0.0.1:5000/get_messages", data={"api_key": api_key,
                                                                                 "sender": "1",
                                                                                 "receiver":
                                                                                     "2"}).text

messages_from_1_to_8 = json.loads(messages_from_1_to_8)
pprint(messages_from_1_to_8)
print(type(messages_from_1_to_8))

print(messages_from_1_to_8[0][0][1])  # receiver
print(messages_from_1_to_8[0][1])  # message
print(messages_from_1_to_8[0][2])  # timestamp

while True:
    message = input('Enter message: ')
    if message == 'exit':
        break
    else:
        print(requests.post('http://127.0.0.1:5000/send_message', data={"api_key": api_key,
                                                                        "sender": "1",
                                                                        "receiver": "2",
                                                                        "message": message}).text)

    messages_from_1_to_8 = requests.post("http://127.0.0.1:5000/get_messages",
                                         data={"api_key": api_key,
                                               "sender": "1",
                                               "receiver":
                                                   "2"}).text
    messages_from_1_to_8 = json.loads(messages_from_1_to_8)

    pprint(messages_from_1_to_8)
