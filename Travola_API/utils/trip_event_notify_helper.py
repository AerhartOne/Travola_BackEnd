from models.trip_event import TripEvent
from datetime import datetime
import time

def notification_check_loop( delay ):
    while True:
        now = datetime.now()
        events_to_notify = TripEvent.select().where( 
                ( now.year - TripEvent.date_time.year == 0) & 
                ( now.month - TripEvent.date_time.month == 0)  &
                ( now.day - TripEvent.date_time.day == 0) &
                ( now.hour - TripEvent.date_time.hour == 0)
            )

        notify_events(events_to_notify)
        time.sleep(delay)

def notify_events( event_list ):
    for e in event_list:
        send_notifications(e)

def send_notifications( target_trip_event ):
    print(f"Sending notifications to {target_trip_event.parent_trip.parent_user.email}")

notification_check_loop(300)