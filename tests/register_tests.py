import database.tools

db = database.tools.Database(r'C:\Users\Flinn\Documents\Chat\Server\server.db',
                             r'C:\Users\Flinn\Documents\Chat\Server\server.pickle')

x = db.add_friend(101, 90)


# db.remove_friend(101, 90)

y = db.get_friends(101)

print(db.is_online(1))

h = db.get_user_of_api_key('ScYSpk8Loj9X1wCbe31cky5-sigcskrE2L8Vrfs2YtOOwbXIcwdJqbAGb5ulUPpNjt1Pqq7Z4QanF7EDlfy8gw')
print(h)



print(x)
print(y)
