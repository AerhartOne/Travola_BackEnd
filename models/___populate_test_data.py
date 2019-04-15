
# Users
from models.user import User
userlist = [
    {
        'username': 'testguy',
        'password': 'asdfasdf',
        'email': 'testguy1@testmail.com',
        'first_name': 'Test',
        'last_name': 'Guy'
    },
    {
        'username': 'guyhero',
        'password': 'asdfasdf',
        'email': 'guyhero@testmail.com',
        'first_name': 'Guy',
        'last_name': 'Hero'
    },
    {
        'username': 'floridaman',
        'password': 'asdfasdf',
        'email': 'floridaman@testmail.com',
        'first_name': 'Florida',
        'last_name': 'Man'
    }
]

for u in userlist:
    if User.get_or_none(User.username == u['username']) == None:
        User.create(
            username=u['username'],
            password=u['password'],
            email=u['email'],
            first_name=u['first_name'],
            last_name=u['last_name']
        )

