from datetime import datetime
from models import db

class JobPosting(db.Model):
    __tablename__ = 'job_postings'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    domain = db.Column(db.String(80), nullable=False)
    experience_required = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100), default='Remote')
    salary_range = db.Column(db.String(80))
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    skill_requirements = db.relationship('JobSkillRequirement', backref='job', lazy=True, cascade='all, delete-orphan')
    applications = db.relationship('Application', backref='job', lazy=True, cascade='all, delete-orphan')

class JobSkillRequirement(db.Model):
    __tablename__ = 'job_skill_requirements'

    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job_postings.id', ondelete='CASCADE'), nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id', ondelete='CASCADE'), nullable=False)
    required_level = db.Column(db.String(50), default='Intermediate')

    skill = db.relationship('Skill', backref='job_requirements', lazy=True)
