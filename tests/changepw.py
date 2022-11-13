import database.tools

db = database.tools.Database(r'C:\Users\Flinn\Documents\Chat\Server\server.db',
                             r'C:\Users\Flinn\Documents\Chat\Server\server.pickle')

# db.add_user('flinnfx',
#            'root@root.com',
#
#            'ba80a53f981c4d0d6a2797b69f12f6e94c212f14685ac4b74b12bb6fdbffa2d17d87c5392aab792dc252d5de4533cc9518d38aa8dbf1925ab92386edd4009923')

db.add_user('tcgamer',
            'tcgamer22@gmail.com',
            '8968535651071498e057c4fe2f71abfc76db12b655c3f7d517be7ff71e5b8273ac6d99df95e6936624f7abca7917fa2724085b7b907f1e7cd1e34594de3c0b4b')

# db.change_password(101,
# 'ba80a53f981c4d0d6a2797b69f12f6e94c212f14685ac4b74b12bb6fdbffa2d17d87c5392aab792dc252d5de4533cc9518d38aa8dbf1925ab92386edd4009923')

db.deactivate(101)
