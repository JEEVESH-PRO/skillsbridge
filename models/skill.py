from models import QueryDescriptor


class Skill:
    _COLLECTION = 'skills'

    def __init__(self, id=None, name=None, category='General'):
        self.id = id
        self.name = name
        self.category = category

    @property
    def courses(self):
        from models.course import Course
        return Course.query.filter_by(skill_id=str(self.id))

    query = QueryDescriptor()

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'category': self.category}

    @staticmethod
    def from_dict(data, doc_id=None):
        return Skill(id=doc_id or data.get('id'), name=data.get('name'), category=data.get('category', 'General'))


class CandidateSkill:
    _COLLECTION = 'candidate_skills'

    def __init__(self, id=None, user_id=None, skill_id=None, proficiency='Intermediate'):
        self.id = id
        self.user_id = user_id
        self.skill_id = skill_id
        self.proficiency = proficiency
        self._skill = None

    @property
    def skill(self):
        if self._skill is None:
            self._skill = Skill.query.get(self.skill_id)
        return self._skill

    @property
    def user(self):
        from models.user import User
        return User.query.get(self.user_id)

    query = QueryDescriptor()

    def to_dict(self):
        return {'id': self.id, 'user_id': self.user_id, 'skill_id': self.skill_id, 'proficiency': self.proficiency}

    @staticmethod
    def from_dict(data, doc_id=None):
        return CandidateSkill(
            id=doc_id or data.get('id'), user_id=data.get('user_id'),
            skill_id=data.get('skill_id'), proficiency=data.get('proficiency', 'Intermediate'),
        )
