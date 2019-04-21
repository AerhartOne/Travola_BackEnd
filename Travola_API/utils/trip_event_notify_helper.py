from models.trip_event import TripEvent
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

def notification_check():
        now = datetime.now()
        events_to_notify = TripEvent.select().where( 
                ( TripEvent.notification_sent == False ) &
                ( now.year - TripEvent.date_time.year == 0) & 
                ( now.month - TripEvent.date_time.month == 0)  &
                ( now.day - TripEvent.date_time.day == 0) &
                ( now.hour - TripEvent.date_time.hour == 0)
            )

        notify_events(events_to_notify)

def notify_events( event_list ):
    for e in event_list:
        send_notifications(e)

def send_notifications( target_trip_event ):
    print(f"{datetime.now()}: Notifying {target_trip_event.parent_trip.parent_user.email} about event {target_trip_event.event_name}, scheduled for {target_trip_event.date_time}")
    # Send email to email address using SendGrid.
    target_trip_event.notification_sent = True
    target_trip_event.save()

scheduler = BackgroundScheduler()
scheduler.add_job(func=notification_check, trigger='interval', seconds=10, start_date=datetime.now() + timedelta(0, 10))
scheduler.start()

atexit.register(lambda: scheduler.shutdown())