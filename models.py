from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    profile = db.relationship('UserProfile', backref='user', uselist=False, cascade="all, delete-orphan")
    trips = db.relationship('Trip', backref='user', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<User {self.username}>'

class UserProfile(db.Model):
    __tablename__ = 'user_profiles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    fullname = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    preferences = db.Column(db.Text, nullable=True) # JSON or serialized text

    def __repr__(self):
        return f'<UserProfile of User ID {self.user_id}>'

class Trip(db.Model):
    __tablename__ = 'trips'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    current_location = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    num_travelers = db.Column(db.Integer, default=1, nullable=False)
    num_days = db.Column(db.Integer, default=1, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    budget = db.Column(db.Float, nullable=False)
    travel_type = db.Column(db.String(50), nullable=False) # Solo, Family, Friends, Couple, Business
    transport_pref = db.Column(db.String(50), nullable=False) # Car, Bus, Train, Flight
    itinerary_data = db.Column(db.Text, nullable=False) # Rich JSON text containing day-by-day plans, hotels, tips, weather, map, checklist
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Trip {self.current_location} to {self.destination}>'
