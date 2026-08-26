from models import db

class Skill(db.Model):
    __tablename__ = 'skills'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    category = db.Column(db.String(80), nullable=False, default='General')

    # Relationships
    courses = db.relationship('Course', backref='skill', lazy=True, cascade='all, delete-orphan')

class CandidateSkill(db.Model):
    __tablename__ = 'candidate_skills'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id', ondelete='CASCADE'), nullable=False)
    proficiency = db.Column(db.String(50), nullable=False, default='Intermediate') # Beginner, Intermediate, Advanced, Expert

    skill = db.relationship('Skill', backref='candidate_associations', lazy=True)
