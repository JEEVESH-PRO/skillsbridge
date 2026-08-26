from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import all models to ensure mapper relationships resolve cleanly
from models.company import Company
from models.skill import Skill, CandidateSkill
from models.user import User
from models.job import JobPosting, JobSkillRequirement
from models.application import Application
from models.course import Course
from models.interview_resource import InterviewResource
