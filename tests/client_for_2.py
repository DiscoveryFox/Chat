import json
from pprint import pprint
import requests

# api_key = requests.post('http://127.0.0.1:5000/auth', data={"id": "2",
#                                                             "password.txt": "password.txt"}).text
with open('api_key_2', 'r') as file:
    #file.write(api_key)
    api_key = file.read()


print(api_key)

while True:
    message = input('Enter message: ')
    if message == 'exit':
        break
    else:
        print('SEND MESSAGE')
        print(requests.post('http://127.0.0.1:5000/send_message', data={"api_key": api_key,
                                                                        "sender": "2",
                                                                        "receiver": "1",
                                                                        "message": message}).text)
        print('MESSAGE SEND')
    print('FETCH MESSAGE')
    messages_from_1_to_8 = requests.post("http://127.0.0.1:5000/get_messages",
                                         data={"api_key": api_key,
                                               "sender": "2",
                                               "receiver":
                                                   "1"}).text
    print(messages_from_1_to_8)
    print(type(messages_from_1_to_8))
    messages_from_1_to_8 = json.loads(messages_from_1_to_8)

    pprint(messages_from_1_to_8)
