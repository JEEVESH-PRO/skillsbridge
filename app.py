import os
import sys

# Import sqlite3 shim if needed
try:
    import sqlite3
except ImportError:
    import database.sqlite3_shim

from flask import Flask, render_template, session, redirect, url_for
from config import Config
from models import db
from database.seed_data import seed_database
from database.firebase_service import init_firebase

# Import blueprints
from routes.auth import auth_bp
from routes.candidate import candidate_bp
from routes.company_search import company_bp
from routes.employer import employer_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # Initialize Firebase Admin SDK (Cloud Firestore & Firebase Auth ready)
    init_firebase()

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(candidate_bp)
    app.register_blueprint(company_bp)
    app.register_blueprint(employer_bp)

    @app.route('/')
    def landing():
        from models.user import User
        from models.job import JobPosting
        from models.company import Company

        user = None
        user_id = session.get('user_id')
        if user_id:
            user = User.query.get(user_id)

        featured_companies = Company.query.limit(5).all()
        recent_jobs = JobPosting.query.order_by(JobPosting.created_at.desc()).limit(4).all()

        return render_template(
            'landing.html',
            user=user,
            companies=featured_companies,
            recent_jobs=recent_jobs
        )

    # Create tables & auto-seed on startup inside app context
    with app.app_context():
        db.create_all()
        seed_database()

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)
