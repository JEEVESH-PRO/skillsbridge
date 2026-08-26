from datetime import datetime
from models import db

class Application(db.Model):
    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job_postings.id', ondelete='CASCADE'), nullable=False)
    status = db.Column(db.String(30), default='Applied') # Applied, Shortlisted, Rejected
    match_score = db.Column(db.Integer, default=0)
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
