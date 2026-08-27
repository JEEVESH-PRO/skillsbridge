from models import QueryDescriptor


class Company:
    _COLLECTION = 'companies'

    def __init__(self, id=None, name=None, industry=None, location=None,
                 logo_url=None, description=None, website=None):
        self.id = id
        self.name = name
        self.industry = industry
        self.location = location
        self.logo_url = logo_url
        self.description = description
        self.website = website

    @property
    def jobs(self):
        from models.job import JobPosting
        return JobPosting.query.filter_by(company_id=str(self.id))

    @property
    def interview_resources(self):
        from models.interview_resource import InterviewResource
        return InterviewResource.query.filter_by(company_id=str(self.id))

    query = QueryDescriptor()

    def to_dict(self):
        return {
            'id': self.id, 'name': self.name, 'industry': self.industry,
            'location': self.location, 'logo_url': self.logo_url,
            'description': self.description, 'website': self.website,
        }

    @staticmethod
    def from_dict(data, doc_id=None):
        return Company(
            id=doc_id or data.get('id'), name=data.get('name'), industry=data.get('industry'),
            location=data.get('location'), logo_url=data.get('logo_url'),
            description=data.get('description'), website=data.get('website'),
        )
