from datetime import datetime
from models import db

class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    provider = db.Column(db.String(100), default='Coursera')
    source_type = db.Column(db.String(50), nullable=False) # youtube, platform, company
    url = db.Column(db.String(500), nullable=False)
    duration = db.Column(db.String(50), default='4 Weeks')
    difficulty = db.Column(db.String(50), default='Intermediate')
    employer_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    employer = db.relationship('User', backref='offered_courses', lazy=True)
