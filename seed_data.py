from app import db, Person, Trip

# Insert sample people
person1 = Person(name="Alice", age=25, location="New York")
person2 = Person(name="Bob", age=30, location="Chicago")

db.session.add_all([person1, person2])
db.session.commit()

# Insert sample trips
trip1 = Trip(person_id=1, cost=2.75, distance=5.0, travel_time=15, mode_of_transport="Subway")
trip2 = Trip(person_id=1, cost=15.0, distance=10.0, travel_time=25, mode_of_transport="Taxi")
trip3 = Trip(person_id=2, cost=1.50, distance=3.0, travel_time=10, mode_of_transport="Bus")

db.session.add_all([trip1, trip2, trip3])
db.session.commit()

print("Sample data inserted successfully!")
