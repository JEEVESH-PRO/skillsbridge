import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'skillsbridge-super-secret-key-2026'
    
    # Detect Netlify / Serverless environment
    IS_NETLIFY = os.environ.get('NETLIFY') is not None or os.environ.get('AWS_LAMBDA_FUNCTION_NAME') is not None
    
    if IS_NETLIFY:
        # In Netlify serverless environment, use /tmp directory for SQLite database if DATABASE_URL is not set
        db_path = os.path.join('/tmp', 'skillsbridge.db')
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'sqlite:///{db_path}'
    else:
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
            'sqlite:///' + os.path.join(BASE_DIR, 'skillsbridge.db')
            
    SQLALCHEMY_TRACK_MODIFICATIONS = False
