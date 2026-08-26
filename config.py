import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'skillsbridge-super-secret-key-2026'
    
    # Detect Vercel serverless environment
    IS_VERCEL = os.environ.get('VERCEL') is not None
    
    if IS_VERCEL:
        # In Vercel serverless environment, use /tmp for SQLite database if DATABASE_URL is not set
        db_path = os.path.join('/tmp', 'skillsbridge.db')
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'sqlite:///{db_path}'
    else:
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
            'sqlite:///' + os.path.join(BASE_DIR, 'skillsbridge.db')
            
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    APP_VERSION = "1.0.0"
