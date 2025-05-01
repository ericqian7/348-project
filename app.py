from flask import Flask, render_template, request, redirect, url_for
from models import db, Trip
from sqlalchemy import text
import os

app = Flask(__name__)
db_path = os.path.join('/tmp', 'trips.db')  # writable path
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    min_cost = request.args.get('min_cost', type=float)

    if min_cost is not None:
        trips = Trip.query.filter(Trip.cost >= min_cost).all()
    else:
        trips = Trip.query.all()

    return render_template('index.html', trips=trips)


@app.route('/report', methods=['GET'])
def report():
    min_cost = request.args.get('min_cost', type=float)
    print("min_cost received:", min_cost)  # debug


    if min_cost is not None:
        # Use prepared statement with min_cost filter
        trips_sql = text("""
            SELECT * FROM trip
            WHERE cost >= :min_cost
        """)
        stats_sql = text("""
            SELECT 
                AVG(cost) AS avg_cost,
                AVG(distance) AS avg_distance,
                AVG(travel_time) AS avg_time
            FROM trip
            WHERE cost >= :min_cost
        """)
        trips = db.session.execute(trips_sql, {"min_cost": min_cost}).fetchall()
        stats = db.session.execute(stats_sql, {"min_cost": min_cost}).fetchone()
    else:
        # Use prepared statement with no filter
        trips_sql = text("SELECT * FROM trip")
        stats_sql = text("""
            SELECT 
                AVG(cost) AS avg_cost,
                AVG(distance) AS avg_distance,
                AVG(travel_time) AS avg_time
            FROM trip
        """)
        trips = db.session.execute(trips_sql).fetchall()
        stats = db.session.execute(stats_sql).fetchone()

    return render_template('report.html', trips=trips, stats=stats, min_cost=min_cost)



@app.route('/add_trip', methods=['GET', 'POST'])
def add_trip():
    if request.method == 'POST':
        # Get data from form
        cost = request.form['cost']
        distance = request.form['distance']
        travel_time = request.form['travel_time']

        # Create a new Trip instance
        new_trip = Trip(cost=cost, distance=distance, travel_time=travel_time)

        # Add and commit to the database
        db.session.add(new_trip)
        db.session.commit()

        return redirect(url_for('index'))  # Redirect back to main page

    return render_template('add_trip.html')  # Render the form to add a trip

@app.route('/edit_trip/<int:id>', methods=['GET', 'POST'])
def edit_trip(id):
    trip = Trip.query.get_or_404(id)

    if request.method == 'POST':
        # Update the trip data
        trip.cost = request.form['cost']
        trip.distance = request.form['distance']
        trip.travel_time = request.form['travel_time']

        # Commit changes to the database
        db.session.commit()

        return redirect(url_for('index'))  # Redirect to the main page

    return render_template('edit_trip.html', trip=trip)

@app.route('/delete_trip/<int:id>', methods=['POST'])
def delete_trip(id):
    trip = Trip.query.get_or_404(id)
    db.session.delete(trip)
    db.session.commit()

    return redirect(url_for('index'))  # Redirect to the main page

if __name__ == '__main__':
    app.run(debug=True)
