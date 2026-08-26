from models import db

class InterviewResource(db.Model):
    __tablename__ = 'interview_resources'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id', ondelete='CASCADE'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job_postings.id', ondelete='SET NULL'), nullable=True)
    title = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    resource_type = db.Column(db.String(50), nullable=False) # Question Bank, System Design, HR Prep, Coding Prep
    description = db.Column(db.Text)

    job = db.relationship('JobPosting', backref='interview_resources', lazy=True)
