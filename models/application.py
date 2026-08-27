from datetime import datetime
from models import QueryDescriptor


class Application:
    _COLLECTION = 'applications'

    def __init__(self, id=None, user_id=None, job_id=None, status='Applied', match_score=0, applied_at=None):
        self.id = id
        self.user_id = user_id
        self.job_id = job_id
        self.status = status
        self.match_score = match_score
        self.applied_at = applied_at or datetime.utcnow()

    @property
    def user(self):
        from models.user import User
        return User.query.get(self.user_id)

    @property
    def job(self):
        from models.job import JobPosting
        return JobPosting.query.get(self.job_id)

    query = QueryDescriptor()

    def to_dict(self):
        return {
            'id': self.id, 'user_id': self.user_id, 'job_id': self.job_id,
            'status': self.status, 'match_score': self.match_score,
            'applied_at': self.applied_at.isoformat() if isinstance(self.applied_at, datetime) else str(self.applied_at),
        }

    @staticmethod
    def from_dict(data, doc_id=None):
        applied = data.get('applied_at')
        if isinstance(applied, str):
            try:
                applied = datetime.fromisoformat(applied)
            except Exception:
                applied = datetime.utcnow()
        return Application(
            id=doc_id or data.get('id'), user_id=data.get('user_id'),
            job_id=data.get('job_id'), status=data.get('status', 'Applied'),
            match_score=data.get('match_score', 0), applied_at=applied,
        )
