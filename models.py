from datetime import datetime
from flask_login import UserMixin
from extensions import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class FarmDiary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    entry_type = db.Column(db.String(50))
    date = db.Column(db.Date)
    crop = db.Column(db.String(100))
    details = db.Column(db.Text)
    amount = db.Column(db.Float, default=0.0)

class TaskPlanner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    task_name = db.Column(db.String(100))
    task_date = db.Column(db.Date)
    task_type = db.Column(db.String(50))
    task_details = db.Column(db.Text)
    is_completed = db.Column(db.Boolean, default=False)

class CropRecommendation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    nitrogen = db.Column(db.Float)
    phosphorus = db.Column(db.Float)
    potassium = db.Column(db.Float)
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    ph = db.Column(db.Float)
    rainfall = db.Column(db.Float)
    recommended_crop = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class FertilizerRecommendation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    nitrogen = db.Column(db.Float)
    phosphorus = db.Column(db.Float)
    potassium = db.Column(db.Float)
    crop_type = db.Column(db.String(100))
    recommended_fertilizer = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
