from datetime import datetime
from models import QueryDescriptor


class Course:
    _COLLECTION = 'courses'

    def __init__(self, id=None, skill_id=None, title=None, provider='Coursera',
                 source_type=None, url=None, duration='4 Weeks', difficulty='Intermediate',
                 employer_id=None, created_at=None):
        self.id = id
        self.skill_id = skill_id
        self.title = title
        self.provider = provider
        self.source_type = source_type
        self.url = url
        self.duration = duration
        self.difficulty = difficulty
        self.employer_id = employer_id
        self.created_at = created_at or datetime.utcnow()

    @property
    def skill(self):
        from models.skill import Skill
        return Skill.query.get(self.skill_id)

    query = QueryDescriptor()

    def to_dict(self):
        return {
            'id': self.id, 'skill_id': self.skill_id, 'title': self.title,
            'provider': self.provider, 'source_type': self.source_type,
            'url': self.url, 'duration': self.duration, 'difficulty': self.difficulty,
            'employer_id': self.employer_id,
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
        return Course(
            id=doc_id or data.get('id'), skill_id=data.get('skill_id'),
            title=data.get('title'), provider=data.get('provider', 'Coursera'),
            source_type=data.get('source_type'), url=data.get('url'),
            duration=data.get('duration', '4 Weeks'), difficulty=data.get('difficulty', 'Intermediate'),
            employer_id=data.get('employer_id'), created_at=created,
        )
