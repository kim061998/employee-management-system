from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, login_manager
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=True)  # Keep for backward compatibility
    password_hash = db.Column(db.String(256), nullable=True)
    role = db.Column(db.String(20), nullable=False, default='encoder')  # Add role attribute

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        self.password = None  # Clear old password field

    def check_password(self, password):
        if self.password_hash:
            return check_password_hash(self.password_hash, password)
        return self.password == password  # Fallback for old passwords

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=False)  # Ensure unique ID
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=True)
    address = db.Column(db.String(200), nullable=True)  # Add address field
    photo = db.Column(db.String(120), nullable=True)  # Add photo field
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
