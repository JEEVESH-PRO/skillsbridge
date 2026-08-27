from datetime import datetime
from models import QueryDescriptor


class JobPosting:
    _COLLECTION = 'job_postings'

    def __init__(self, id=None, company_id=None, title=None, domain=None,
                 experience_required=None, location='Remote', salary_range=None,
                 description=None, created_at=None):
        self.id = id
        self.company_id = company_id
        self.title = title
        self.domain = domain
        self.experience_required = experience_required
        self.location = location
        self.salary_range = salary_range
        self.description = description
        self.created_at = created_at or datetime.utcnow()

    @property
    def skill_requirements(self):
        return JobSkillRequirement.query.filter_by(job_id=str(self.id))

    @property
    def company(self):
        from models.company import Company
        return Company.query.get(self.company_id)

    @property
    def applications(self):
        from models.application import Application
        return Application.query.filter_by(job_id=str(self.id))

    query = QueryDescriptor()

    def to_dict(self):
        return {
            'id': self.id, 'company_id': self.company_id, 'title': self.title,
            'domain': self.domain, 'experience_required': self.experience_required,
            'location': self.location, 'salary_range': self.salary_range,
            'description': self.description,
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
        return JobPosting(
            id=doc_id or data.get('id'), company_id=data.get('company_id'),
            title=data.get('title'), domain=data.get('domain'),
            experience_required=data.get('experience_required'),
            location=data.get('location', 'Remote'), salary_range=data.get('salary_range'),
            description=data.get('description'), created_at=created,
        )


class JobSkillRequirement:
    _COLLECTION = 'job_skill_requirements'

    def __init__(self, id=None, job_id=None, skill_id=None, required_level='Intermediate'):
        self.id = id
        self.job_id = job_id
        self.skill_id = skill_id
        self.required_level = required_level
        self._skill = None

    @property
    def skill(self):
        if self._skill is None:
            from models.skill import Skill
            self._skill = Skill.query.get(self.skill_id)
        return self._skill

    query = QueryDescriptor()

    def to_dict(self):
        return {'id': self.id, 'job_id': self.job_id, 'skill_id': self.skill_id, 'required_level': self.required_level}

    @staticmethod
    def from_dict(data, doc_id=None):
        return JobSkillRequirement(
            id=doc_id or data.get('id'), job_id=data.get('job_id'),
            skill_id=data.get('skill_id'), required_level=data.get('required_level', 'Intermediate'),
        )
