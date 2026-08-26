from models import db

class Company(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    industry = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(120))
    logo_url = db.Column(db.String(256))
    description = db.Column(db.Text)
    website = db.Column(db.String(256))

    # Relationships
    jobs = db.relationship('JobPosting', backref='company', lazy=True, cascade='all, delete-orphan')
    interview_resources = db.relationship('InterviewResource', backref='company', lazy=True, cascade='all, delete-orphan')
