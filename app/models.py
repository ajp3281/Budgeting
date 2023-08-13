from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self,password):
        self.password_hash = generate_password_hash(password)
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)
    frequency = db.Column(db.String(50), nullable=True) # e.g., "monthly", "weekly"

class Expenses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    expenses = db.relationship('Expenses', backref='category', lazy=True)