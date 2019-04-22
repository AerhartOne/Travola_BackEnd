from models.trip_event import TripEvent
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

sg = SendGridAPIClient( os.getenv("SENDGRID_API_KEY") )

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

    message = Mail(
        from_email='no-reply@travola.com',
        to_emails=target_trip_event.parent_trip.parent_user.email,
        subject="You have an event now!",
        html_content=f"<h1>You have an event to go to!</h1> <p><h2>{target_trip_event.event_name}</h2></p> <p><h3>Date/Time: {target_trip_event.date_time}</h3></p> <p><h3>Location: {target_trip_event.location}</h3></p>"
    )

    try:
        sg.send(message)
        print(f"Sent mail to {target_trip_event.parent_trip.parent_user.email} about event {target_trip_event.event_name}!")
        target_trip_event.notification_sent = True
        target_trip_event.save()
    except Exception as e:
        print(f"Couldn't send mail notification to {target_trip_event.parent_trip.parent_user.email} about event {target_trip_event.event_name}!")
        print(e)


scheduler = BackgroundScheduler({
    'apscheduler.job_defaults.max_instances': 1,
    'apscheduler.executors.default': {
        'class': 'apscheduler.executors.pool:ThreadPoolExecutor',
        'max_workers': '1'
    },
})


scheduler.add_job(func=notification_check, trigger='interval', minutes=2, start_date=datetime.now() + timedelta(0, 10))
scheduler.start()

atexit.register(lambda: scheduler.shutdown())