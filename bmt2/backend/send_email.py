import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ssl

from celery.schedules import crontab
from datetime import datetime, time
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from model import User, Show, Booking, Theatre
import datetime as dt
from flask import render_template_string
import csv
app_ = Flask(__name__)
app_.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
basedir = os.path.abspath(os.path.dirname(__file__))
app_.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')

db = SQLAlchemy(app_)

from my_celery import celery_app


@celery_app.task(name="send_daily_reminder_email")
def send_daily_reminder_email():
    port = 465  # For SSL
    password = 'tcdiogedheyogrry'  # This should be  email's app password
    subject = 'Daily Reminder: Book a Show!'
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        try:
            server.login("shubhankarplay@gmail.com", password)
            
            sender_email = "shubhankarplay@gmail.com"
            
            with app_.app_context():
                # Get users who haven't booked in the last 24 hours
                current_time = datetime.utcnow()
                last_24_hours = current_time - dt.timedelta(hours=24)
                users = db.session.query(User).filter(User.last_booked <= last_24_hours).all()
                
                for user in users:
                    # Update the message to include the user's name
                    message = f"Hi {user.username}! It looks like you haven't booked any show in the last 24 hours. Why not explore our latest shows and book your tickets today?"
                    email_content = f"Subject: {subject}\n\n{message}"
                    server.sendmail(sender_email, user.email, email_content)
            
            print("Daily reminder emails sent successfully")
        except Exception as e:
            print("Error sending daily reminder emails:", e)

   
@celery_app.task(name="send_monthly_report")
def send_monthly_report():
    subject = 'text subject'
    message='test message'
    port = 465  # For SSL
    password = 'tcdiogedheyogrry'  # This should be  email's app password
    
    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        try:
            server.login("shubhankarplay@gmail.com", password)
            
            sender_email = "shubhankarplay@gmail.com"
            with app_.app_context():
                users = db.session.query(User).all()
                for user in users:
                    recipients = [user.email]
                    report_content = generate_user_booking_report(user)
                   
                    
                    msg = MIMEMultipart()
                    msg['Subject'] = subject
                    msg['From'] = sender_email
                    msg['To'] = ', '.join(recipients)

                    # Attach the HTML report
                    attachment = MIMEText(report_content, 'html')
                    msg.attach(attachment)

                    server.sendmail(sender_email, recipients, msg.as_string())
            
            print("Emails sent successfully")
        except Exception as e:
            print("Error sending emails:", e)

celery_app.conf.beat_schedule = {
        'send_email_task': {
            'task': 'send_monthly_report',
        'schedule': crontab(day_of_month='13', hour=19, minute=5), 
            
        },
          'send_daily_reminder_task': {
        'task': 'send_daily_reminder_email',
        'schedule': crontab(hour=19, minute=5),  
    },
    }




def generate_user_booking_report(user):
    
    with app_.app_context(): 
        bookings = db.session.query(Booking).filter_by(user_id=user.id).all()

        # Generate the HTML report content
        report_content = render_template_string("""
            <html>
            <head>
                <title>Booking Report for {{ user.username }}</title>
            </head>
            <body>
                <h1>Booking Report for {{ user.username }}</h1>
                <ul>
                    {% for booking in bookings %}
                        <li>
                            Movie: {{ booking.shows_backref.name }} |
                            Tickets: {{ booking.num_tickets }} |
                            Total Price: ${{ booking.total_price }}
                        </li>
                    {% endfor %}
                </ul>
            </body>
            </html>
        """, user=user, bookings=bookings)

        return report_content


@celery_app.task
def export_theatre_csv(theatre_id):
    theatre = db.session.query(Theatre).get(theatre_id)
    if theatre:
        shows = Show.query.filter_by(theatre_id=theatre.id).all()

        # Generate CSV data
        csv_data = []
        for show in shows:
            csv_data.append([show.name, show.rating, show.genres, show.ticket_price])

        # Write CSV data to a file
        csv_filename = f'theatre_{theatre_id}_details.csv'
        with open(csv_filename, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['Show Name', 'Rating', 'Genres', 'Ticket Price'])
            writer.writerows(csv_data)

        return csv_filename
    else:
        return None