import time

import models

data: dict = {'Message': 'This is a test message',
              'SendTime': time.time(),
              'ApiKey': 'somerandomapikey',
              'To': 'Marc#102'}

message = models.ClassicMessage(data)

x = models.ForwardingClassicMessage(message, 2)
