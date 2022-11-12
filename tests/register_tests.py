import database.tools

db = database.tools.Database(r'C:\Users\Flinn\Documents\Chat\Server\server.db',
                             r'C:\Users\Flinn\Documents\Chat\Server\server.pickle')

x = db.add_friend(101, 90)


# db.remove_friend(101, 90)

y = db.get_friends(101)

print(db.is_online(1))

print(x)
print(y)
