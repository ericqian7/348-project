from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cost = db.Column(db.Float, nullable=False)
    distance = db.Column(db.Float, nullable=False)
    travel_time = db.Column(db.Float, nullable=False)
    __table_args__ = (
        db.Index('idx_trip_cost', 'cost'),
    )

    def __repr__(self):
        return f'<Trip {self.id}>'
