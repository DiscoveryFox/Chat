import requests

response = requests.post('http://127.0.0.1:5000/register', data={"username": "Flinn",
                                                                 "email": "flinn.handymail@gmail.com",
                                                                 "password.txt": "123"})

print(response.text)
