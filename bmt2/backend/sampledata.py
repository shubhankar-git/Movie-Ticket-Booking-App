from datetime import datetime
import datetime as dt
from app import db, User 
from flask import Flask, current_app
import os, json
import random
from model import User, Role, Theatre, Show, Booking
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')

# ... Flask app configuration ...

db = SQLAlchemy(app)

with app.app_context():

    def generate_user_data():
        for _ in range(50):
            username = random.choice(['johndoe', 'janedoe', 'smith', 'jones', 'miller']) + str(_)
            email = username + str(_) + '@example.com'
            password = 'password'
            last_booked = datetime.utcnow() - random.randint(1, 30) * dt.timedelta(days=1)
            user = User(username=username, email=email, password=password, last_booked=last_booked)
            db.session.add(user)

    def generate_theatre_data():
        for _ in range(10):
            name = random.choice(['Theater 1', 'Theater 2', 'Theater 3', 'Theater 4', 'Theater 5'])
            place = random.choice(['New York City', 'Los Angeles', 'Chicago', 'San Francisco', 'Miami'])
            capacity = random.randint(100, 1000)
            theatre = Theatre(name=name, place=place, capacity=capacity)
            db.session.add(theatre)

    def generate_show_data():
        for theatre in db.session.query(Theatre).all():
            for _ in range(2, 5):
                name = random.choice(['The Lion King', 'The Phantom of the Opera', 'Hamilton', 'Wicked', 'Les Miserables'])
                rating = round(random.uniform(1.0, 5.0), 1)
                genres_list = random.choices(['Comedy', 'Action', 'Sci-Fi', 'Romance', 'Horror', 'Drama', 'Fantasy'], k=3)
                genres = json.dumps(genres_list)
                ticket_price = round(random.uniform(50.0, 100.0))
                show = Show(name=name, rating=rating, genres=genres, ticket_price=ticket_price, theatre_id=theatre.id)
                db.session.add(show)

    def generate_booking_data():
        for user in db.session.query(User).all():
            for show in db.session.query(Show).all():
                num_tickets = random.randint(1, 10)
                total_price = 200 * num_tickets
                booking = Booking(user_id=user.id, show_id=show.id, num_tickets=num_tickets, total_price=total_price, shows=show)
                db.session.add(booking)

    generate_user_data()
    generate_theatre_data()
    generate_show_data()
    generate_booking_data()
    db.session.commit()
    print("User added successfully.")


def generate_admin():
    try:
        with app.app_context():
            admin_role = db.session.query(Role).filter_by(name='admin').first()
            if not admin_role:
                admin_role = Role(name='admin', description='Administrator Role')
                db.session.add(admin_role)
                db.session.commit()

            # Create the admin user if it doesn't exist
            admin_user = db.session.query(User).filter_by(username='admin').first()
            if not admin_user:
                last_booked = datetime.utcnow() - random.randint(1, 30) * dt.timedelta(days=1)
                admin_user = User(username='admin', password='adminpassword', email='example@xyz', last_booked=last_booked)
                admin_user.roles.append(admin_role)
                db.session.add(admin_user)
                db.session.commit()
                print('success')

    except Exception as e:
        print("An error occurred:", e)


generate_admin()
