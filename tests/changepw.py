import database.tools
db = database.tools.Database(r'C:\Users\Flinn\Documents\Chat\Server\server.db',
                             r'C:\Users\Flinn\Documents\Chat\Server\server.pickle')
# db.change_password(101,
# 'ba80a53f981c4d0d6a2797b69f12f6e94c212f14685ac4b74b12bb6fdbffa2d17d87c5392aab792dc252d5de4533cc9518d38aa8dbf1925ab92386edd4009923')

db.deactivate(101)