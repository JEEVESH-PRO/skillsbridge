from models import QueryDescriptor


class InterviewResource:
    _COLLECTION = 'interview_resources'

    def __init__(self, id=None, company_id=None, job_id=None, title=None,
                 url=None, resource_type=None, description=None):
        self.id = id
        self.company_id = company_id
        self.job_id = job_id
        self.title = title
        self.url = url
        self.resource_type = resource_type
        self.description = description

    @property
    def company(self):
        from models.company import Company
        return Company.query.get(self.company_id)

    query = QueryDescriptor()

    def to_dict(self):
        return {
            'id': self.id, 'company_id': self.company_id, 'job_id': self.job_id,
            'title': self.title, 'url': self.url,
            'resource_type': self.resource_type, 'description': self.description,
        }

    @staticmethod
    def from_dict(data, doc_id=None):
        return InterviewResource(
            id=doc_id or data.get('id'), company_id=data.get('company_id'),
            job_id=data.get('job_id'), title=data.get('title'),
            url=data.get('url'), resource_type=data.get('resource_type'),
            description=data.get('description'),
        )
