import hashlib

import faker
import database.tools

fake = faker.Faker()

database = database.tools.Database(r'C:\Users\Flinn\Documents\Chat\Server\server.db')
# '''
for x in range(100):
    name = fake.name()
    email = fake.email()
    password = fake.password()
    hashed_password = hashlib.blake2b(bytes(password, 'utf-8')).hexdigest()
    print(f'{x}: {name} {email} {password}')
    database.add_user(name, email, hashed_password)
# '''
'''
if input('Continue: ') == 'y':
    for x in range(int(input('How many users: '))):
        print(f'{x}: {database.generate_api_key(x)}')
    else:
        print('Done')
'''
# for x in range(100):
#    print(database.check_api_key(1, database.get_api_key(x)))

# print(database.check_api_key(1,
#                             "vNJbstIQY-sm9m0qJd-VcMl3z3hhWUg_c0qbjo_xi0aDYyF4RCX1jDzdPDsW
#                             -Q9Tmsbc-25To5uSFE2qJk3DOQ"))

'''
for x in range(100):
    text = fake.text()
    print(f'{x}: {text}')
    database.add_message([1, 3], text)
'''

# print(database.get_contacts(1))

# print(database.check_contact(1, 55))

#
'''
print(database.get_api_key(4))
print(database.update_api_key(4))
print(database.get_api_key(4))
'''

'''pprint(database.get_messages(3, 1))
print(len(database.get_messages(3, 1)))'''

'''print(database.get_contacts(8))
print(database.get_contacts(1))

print(database.add_contact(1, 8))

print(database.get_contacts(1))
print(database.get_contacts(8))

database.add_contact(2, 1)
'''

# change password.txt for user with ID 1
print(database.change_password(101,
                               'ba80a53f981c4d0d6a2797b69f12f6e94c212f14685ac4b74b12bb6fdbffa2d17d87c5392aab792dc252d5de4533cc9518d38aa8dbf1925ab92386edd4009923'))

print(database.change_password(2,
                                '7c863950ac93c93692995e4732ce1e1466ad74a775352ffbaaf2a4a4ce9b549d0b414a1f3150452be6c7c72c694a7cb46f76452917298d33e67611f0a42addb8'))

database.authenticate(1)

database.authenticate(2)
