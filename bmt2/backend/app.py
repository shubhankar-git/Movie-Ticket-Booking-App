import os
import time
import json
from flask import Flask,  request,  jsonify,make_response
from io import BytesIO
from flask_migrate import Migrate
from datetime import datetime
from flask_caching import Cache

from sqlalchemy.orm import joinedload

from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

from flask_marshmallow import Marshmallow
from flask_cors import CORS, cross_origin



app = Flask(__name__)
CORS(app,resources={r"/*": {"origins": "*"}},supports_credentials=True)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SECURITY_PASSWORD_SALT'] = 'your_salt_value_here'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
mm = Marshmallow(app)
jwt = JWTManager(app)
from model import db, User, Role, Theatre, Show, Booking, CsvEntry






# Setup Flask-Security



migrate = Migrate(app, db)

class UserSchema(mm.Schema):
    class Meta:
        fields=("id", "username", "password","email")

user_schema = UserSchema()







@app.route('/register', methods=['POST'])
@cross_origin(supports_credentials=True)
def register():
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']
    existing_user = User.query.filter_by(username=username).first()
    existing_mail = User.query.filter_by(email=email).first()
    if existing_user:
        return {'message': 'Username already exists'}, 409
    if existing_mail:
        return {'message': 'Email already exists'}, 500
    
    new_user = User(username=username, password=password, email=email,last_booked= None)
    
    db.session.add(new_user)
    db.session.commit()
    serialized_user = user_schema.dump(new_user)

    response = jsonify(serialized_user)
   
    return response, 201





# Custom route for admin promotion
@app.route('/promote', methods=['POST'])
@jwt_required()
def promote_user():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if not current_user or not any(role.name == 'admin' for role in current_user.roles):
        return jsonify({'message': 'Unauthorized'}), 401

    data = request.get_json()
    username_or_user_id = data.get('usernameOrUserId')

    user = User.query.filter_by(username=username_or_user_id).first()
    if user is None:
        user = User.query.get(username_or_user_id)

    if user is None:
        return jsonify({'message': 'User not found.'}), 404

    admin_role = Role.query.filter_by(name='admin').first()
    if admin_role:
        user.roles.append(admin_role)
        db.session.commit()
        return jsonify({'message': f'User {user.username} has been promoted to admin.'}), 200
    else:
        return jsonify({'message': 'Admin role not found.'}), 500


# Routes for login and signup
@app.route('/login', methods=['POST'])
@cross_origin(supports_credentials=True)
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        roles = [role.name for role in user.roles]
        access_token = create_access_token(identity=user.id, additional_claims={'roles': roles})
        return jsonify({'access_token': access_token, 'roles': roles, 'username':username}), 200

    else:
        return jsonify({'message': 'Invalid credentials'}), 401


@app.route('/admin/theatres', methods=['POST'])
@cross_origin(supports_credentials=True)
@jwt_required()  # To ensure only authenticated users with a valid JWT can access this route
def create_theatre():
    # Check if the current user has admin role
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if not current_user or not any(role.name == 'admin' for role in current_user.roles):
        return jsonify({'message': 'Unauthorized'}), 401

    # Parse the request data to get theatre details
    data = request.get_json()
    name = data.get('name')
    place = data.get('place')
    capacity = data.get('capacity')

    # Create a new Theatre object and save it to the database
    new_theatre = Theatre(name=name, place=place, capacity=capacity)
    db.session.add(new_theatre)
    db.session.commit()

    return jsonify({'message': 'Theatre created successfully'}), 201

class TheatreSchema(mm.Schema):
    class Meta:
        fields = ("id", "name", "place", "capacity")

theatre_schema = TheatreSchema()
@app.route('/gettheatres', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_theatres():
    theatres = Theatre.query.all()
    theatres_list = [{'id': theatre.id, 'name': theatre.name, 'place': theatre.place, 'capacity': theatre.capacity} for theatre in theatres]
    return jsonify(theatres_list)


@app.route('/admin/theatres/<int:theatreid>/add_show', methods=['POST'])
@cross_origin(supports_credentials=True)
@jwt_required()
def add_show(theatreid):
    # Check if the current user has admin role
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if not current_user or not any(role.name == 'admin' for role in current_user.roles):
        return jsonify({'message': 'Unauthorized'}), 401

    # Parse the request data to get show details
    data = request.get_json()
    name = data.get('name')
    rating = float(data.get('rating'))
    genres = data.get('genres')
    genres_str = json.dumps(genres)
    ticket_price = data.get('ticket_price')

    # Check if the theatre exists
    theatre = Theatre.query.get(theatreid)
    if not theatre:
        return jsonify({'message': 'Theatre not found'}), 404

    # Create a new Show object and associate it with the theatre
    new_show = Show(name=name, rating=rating, genres=genres_str, ticket_price=ticket_price, theatre_id=theatreid)
    db.session.add(new_show)
    db.session.commit()

    return jsonify({'message': 'Show added successfully'}), 201

@app.route('/edittheatre/<int:theatre_id>', methods=['PUT'])
@jwt_required()
def edit_theatre(theatre_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if not current_user or not any(role.name == 'admin' for role in current_user.roles):
        return jsonify({'message': 'Unauthorized'}), 401
    data = request.get_json()
    new_name = data.get('name')

    theatre = Theatre.query.get(theatre_id)
    if theatre:
        theatre.name = new_name
        db.session.commit()
        return jsonify({'message': 'Theatre name updated successfully'})
    else:
        return jsonify({'message': 'Theatre not found'}), 404
    
@app.route('/deletetheatre/<int:theatre_id>', methods=['DELETE'])
@jwt_required()
def delete_theatre(theatre_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if not current_user or not any(role.name == 'admin' for role in current_user.roles):
        return jsonify({'message': 'Unauthorized'}), 401
    theatre = Theatre.query.get(theatre_id)
    if theatre:
        db.session.delete(theatre)
        db.session.commit()
        return jsonify({'message': 'Theatre deleted successfully'})
    else:
        return jsonify({'message': 'Theatre not found'}), 404
    

@app.route('/getshows', methods=['GET'])
@jwt_required()
def get_shows():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if not current_user or not any(role.name == 'admin' for role in current_user.roles):
        return jsonify({'message': 'Unauthorized'}), 401
    theaters = Theatre.query.all()
    theater_list = []  # Initialize as an empty list

    for theater in theaters:
        theater_data = {
            "id": theater.id,
            "name": theater.name,
            "shows": []
        }

        shows = Show.query.filter_by(theatre_id=theater.id).all()
        for show in shows:
            show_data = {
                "id": show.id,
                "name": show.name,
                "rating": show.rating,
                'genres': json.loads(show.genres),
                "ticket_price": show.ticket_price
            }
            theater_data["shows"].append(show_data)

        theater_list.append(theater_data)  # Append theater_data to the list
    
    return jsonify(theater_list)

# Edit show details
@app.route('/editshow/<int:show_id>', methods=['PUT'])
@jwt_required()
def edit_show(show_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if not current_user or not any(role.name == 'admin' for role in current_user.roles):
        return jsonify({'message': 'Unauthorized'}), 401
    show = Show.query.get_or_404(show_id)
    
    show.name = request.json.get('name', show.name)
    show.rating = request.json.get('rating', show.rating)
    genres = request.json.get('genres', show.genres)
    show.genres = json.dumps(genres)
    show.ticket_price = request.json.get('ticket_price', show.ticket_price)
    
    try:
        db.session.commit()
        return jsonify({"message": "Show edited successfully"}), 200
    except:
        db.session.rollback()
        return jsonify({"message": "Error editing show"}), 500

# Delete a show
@app.route('/deleteshow/<int:show_id>', methods=['DELETE'])
@jwt_required()
def delete_show(show_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if not current_user or not any(role.name == 'admin' for role in current_user.roles):
        return jsonify({'message': 'Unauthorized'}), 401
    show = Show.query.get_or_404(show_id)
    
    try:
        show = Show.query.get(show_id)
        if not show:
            return jsonify({'message': 'Show not found'}), 404

        # Delete associated bookings
        bookings = Booking.query.filter_by(show_id=show_id).all()
        for booking in bookings:
            db.session.delete(booking)

        db.session.delete(show)
        db.session.commit()
        return jsonify({'message': 'Show and associated bookings deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error deleting show and associated bookings'}), 500





    

@app.route('/user/dashboard', methods=['GET'])
@cross_origin(supports_credentials=True)
@jwt_required()
@cache.cached(timeout=60)
def user_dashboard():
    # Fetch all theatres and their associated shows
    theatres = Theatre.query.all()
    theatres_data = []
    for theatre in theatres:
        shows = Show.query.filter_by(theatre_id=theatre.id).all()
        shows_data = []
        for show in shows:
            theatre = Theatre.query.get(show.theatre_id)
            total_tickets_booked = sum(booking.num_tickets for booking in show.bookings)
            available_seats = theatre.capacity - total_tickets_booked,
            is_house_full = total_tickets_booked >= theatre.capacity
            show_data = {
                'id': show.id,
                'name': show.name,
                'rating': show.rating,
                'genres': json.loads(show.genres),
                'ticket_price': show.ticket_price,
                'available_seats': available_seats,
                'is_house_full': is_house_full
            }
            shows_data.append(show_data)
        theatre_data = {
            'id': theatre.id,
            'name': theatre.name,
            'place': theatre.place,
            'capacity': theatre.capacity,
            'shows': shows_data
        }
        theatres_data.append(theatre_data)
    return jsonify(theatres_data)

@app.route('/bookings/<int:showId>', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
@jwt_required()
def book_tickets(showId):
    if request.method == 'POST':
        data = request.get_json()
        num_tickets = data.get('numTickets')

        current_user_id = get_jwt_identity()
        if not current_user_id:
            return jsonify({'message': 'Authentication required'}), 401

        show = Show.query.get(showId)
    
        if not show:
            return jsonify({'message': 'Show not found'}), 404
        theatre = Theatre.query.get(show.theatre_id)
        total_tickets_booked = sum(booking.num_tickets for booking in show.bookings)
        
        if total_tickets_booked >= theatre.capacity:
            return jsonify({'message': 'House full! No more tickets available for booking'}), 400

        if num_tickets <= 0 or num_tickets > (theatre.capacity - total_tickets_booked):
            return jsonify({'message': 'Invalid number of tickets'}), 400

        total_price = num_tickets * show.ticket_price
        new_booking = Booking(user_id=current_user_id, show_id=showId, num_tickets=num_tickets, total_price=total_price,shows=show)
        
        db.session.add(new_booking)
        db.session.commit()
        user = User.query.get(current_user_id)
        user.last_booked = datetime.utcnow()
        db.session.commit()


        return jsonify({'message': f'{num_tickets} tickets booked successfully! Total price: ${total_price}'}), 201

    elif request.method == 'GET':
        # Fetch the show details
        show = Show.query.get(showId)
        theatre = Theatre.query.get(show.theatre_id)
        total_tickets_booked = sum(booking.num_tickets for booking in show.bookings)
        if not show:
            return jsonify({'message': 'Show not found'}), 404

        # You can return the show details as JSON or any other format you desire
        return jsonify({
            'id': show.id,
            'name': show.name,
            'rating': show.rating,
            'genres': json.loads(show.genres),
            'ticket_price': show.ticket_price,
            'available_seats': theatre.capacity - total_tickets_booked,
            'is_house_full': False,
            # Add other show details here
        }), 200

@app.route('/user/booked-tickets', methods=['GET'])
@jwt_required()
def get_user_booked_tickets():
    current_user_id = get_jwt_identity()

    booked_tickets = Booking.query.filter_by(user_id=current_user_id).all()
    booked_tickets_data = []
    for ticket in booked_tickets:
        show = Show.query.get(ticket.show_id)
        if show:
            # Append the ticket data along with show details to the list
            booked_tickets_data.append({
                'show_id': show.id,
                'show_name': show.name,
                'num_tickets': ticket.num_tickets,
                'total_price': ticket.total_price,
                # Add other ticket details as needed
            })
        else:
            # If the show is not found (possibly deleted), handle the situation as needed
            print(f"Show with ID {ticket.show_id} not found for booking ID {ticket.id}")

    return jsonify(booked_tickets_data), 200








    
 
@app.route('/exportTheatres', methods=['GET'])
@jwt_required()
def exportTheatres():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if not current_user or not any(role.name == 'admin' for role in current_user.roles):
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401

    theatres = Theatre.query.all()
    theatre_list = []
    
    for theatre in theatres:
        theatre_data = {
            'id': theatre.id,
            'name': theatre.name,
        }
        theatre_list.append(theatre_data)
    
    return jsonify(theatre_list)



from exportCSV import export_theatre_csv
@app.route('/export-csv/<int:theatre_id>')
def export_csv_route(theatre_id):
    export_task = export_theatre_csv.delay(theatre_id)
    response_data = {
        'message': f"Export task for Theatre ID {theatre_id} initiated with task ID: {export_task.id}",
       
    }
    return jsonify(response_data)

@app.route('/download-csv/<int:selectedTheatre>', methods=['GET'])
def download_csv(selectedTheatre):
    try:
        # Retrieve the CSV data from the database using the selected theatre ID
        csv_entry = CsvEntry.query.filter_by(theatre_id=selectedTheatre).first()
        
        if csv_entry:
            csv_data = csv_entry.content  # Get the CSV data

            # Set up the response headers for CSV download
            response = make_response(csv_data)
            response.headers['Content-Disposition'] = f'attachment; filename=theatre_ID{selectedTheatre}_details.csv'
            response.mimetype = 'text/csv'

            return response
        else:
            return jsonify({'message': 'CSV data not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def create_app():
    db.init_app(app) 
    # Inside app.app_context(), create the database tables
    with app.app_context():
        db.create_all()
    
    return app
if __name__ == '__main__':
     app = create_app()
     app.run(debug=True)
