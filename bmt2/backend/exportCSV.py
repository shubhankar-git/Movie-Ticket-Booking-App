from celery import Celery
from celery.schedules import crontab
from datetime import datetime, time
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from model import User, Show, Booking, Theatre, CsvEntry
import datetime as dt
from flask import render_template_string
import csv
from my_celery import celery_app
app_ = Flask(__name__)
app_.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
basedir = os.path.abspath(os.path.dirname(__file__))
app_.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
db = SQLAlchemy(app_)


@celery_app.task
def export_theatre_csv(theatre_id):
     with app_.app_context():
        theatre = db.session.query(Theatre).get(theatre_id)

        if theatre:
            shows = db.session.query(Show).filter_by(theatre_id=theatre.id).all()

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

            csv_content = ''
            with open(csv_filename, 'rb') as csv_file:
                csv_file = csv_file.read()
        
            
            csv_entry = CsvEntry(theatre_id=theatre.id, content=csv_file,filename=csv_filename)
            db.session.query(CsvEntry).delete()
            db.session.add(csv_entry)
            db.session.commit()

            # Delete the temporary CSV file
            os.remove(csv_filename)

            return 'CSV exported successfully'
        else:
            return 'Theatre not found', 404