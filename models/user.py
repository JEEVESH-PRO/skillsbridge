from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from models import QueryDescriptor


class User:
    _COLLECTION = 'users'

    def __init__(self, id=None, name=None, email=None, password_hash=None,
                 role='candidate', headline=None, bio=None, company_id=None, created_at=None):
        self.id = id
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.role = role
        self.headline = headline
        self.bio = bio
        self.company_id = company_id
        self.created_at = created_at or datetime.utcnow()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_employer(self):
        return self.role == 'employer'

    def is_candidate(self):
        return self.role == 'candidate'

    @property
    def candidate_skills(self):
        from models.skill import CandidateSkill
        return CandidateSkill.query.filter_by(user_id=str(self.id))

    @property
    def applications(self):
        from models.application import Application
        return Application.query.filter_by(user_id=str(self.id))

    @property
    def employer_company(self):
        if self.company_id:
            from models.company import Company
            return Company.query.get(self.company_id)
        return None

    query = QueryDescriptor()

    def to_dict(self):
        return {
            'id': self.id, 'name': self.name, 'email': self.email,
            'password_hash': self.password_hash, 'role': self.role,
            'headline': self.headline, 'bio': self.bio, 'company_id': self.company_id,
            'created_at': self.created_at.isoformat() if isinstance(self.created_at, datetime) else str(self.created_at),
        }

    @staticmethod
    def from_dict(data, doc_id=None):
        created = data.get('created_at')
        if isinstance(created, str):
            try:
                created = datetime.fromisoformat(created)
            except Exception:
                created = datetime.utcnow()
        return User(
            id=doc_id or data.get('id'), name=data.get('name'), email=data.get('email'),
            password_hash=data.get('password_hash'), role=data.get('role', 'candidate'),
            headline=data.get('headline'), bio=data.get('bio'),
            company_id=data.get('company_id'), created_at=created,
        )
