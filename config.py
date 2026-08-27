import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'skillsbridge-super-secret-key-2026'
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
