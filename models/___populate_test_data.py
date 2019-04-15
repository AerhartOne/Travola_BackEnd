
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



# Trips
from models.trip import Trip
triplist =[
    {
        'trip_name' : 'Working in Europe',
        'parent_user' : User.select().first().id
    },
    {
        'trip_name' : 'Guy Things',
        'parent_user' : User.select().first().id + 1
    },
    {
        'trip_name' : 'Heroic Things',
        'parent_user' : User.select().first().id + 1
    },
    {
        'trip_name' : 'Florida Trip',
        'parent_user' : User.select().first().id + 2
    }
]

for t in triplist:
    if Trip.get_or_none(Trip.trip_name == t['trip_name']) == None:
        Trip.create(
            trip_name = t['trip_name'],
            parent_user = t['parent_user']
        )

# Trip Events
from models.trip_event import TripEvent
from datetime import datetime

tripevent_list = [
    {
        'parent_trip' : Trip.select().first().id,
        'date_time' : datetime(2019, 8, 12),
        'location' : 'Berlin'
    },
    {
        'parent_trip' : Trip.select().first().id,
        'date_time' : datetime(2019, 7, 23),
        'location' : 'Frankfurt'
    },
    {
        'parent_trip' : Trip.select().first().id + 1,
        'date_time' : datetime(2019, 4, 18),
        'location' : 'California'
    },
    {
        'parent_trip' : Trip.select().first().id + 2,
        'date_time' : datetime(2019, 3, 22),
        'location' : 'Arizona'
    },
    {
        'parent_trip' : Trip.select().first().id + 3,
        'date_time' : datetime(2019, 4, 2),
        'location' : 'Florida'
    }
]

for te in tripevent_list:
    if TripEvent.get_or_none(TripEvent.parent_trip == te['parent_trip']) == None:
        TripEvent.create(
            parent_trip=te['parent_trip'],
            date_time=te['date_time'],
            location=te['location']
        )