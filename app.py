import os
from flask import Flask, render_template, session, url_for
from config import Config
from database import sqlite_db, sqlite_seed

from routes.auth import auth_bp
from routes.candidate import candidate_bp
from routes.company_search import company_bp
from routes.employer import employer_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    sqlite_db.init_db()
    sqlite_seed.seed_database()

    app.register_blueprint(auth_bp)
    app.register_blueprint(candidate_bp)
    app.register_blueprint(company_bp)
    app.register_blueprint(employer_bp)

    @app.after_request
    def add_header(response):
        # Enable high-speed caching for static CSS/JS/images
        if 'static' in str(response.headers.get('Content-Type', '')):
            response.headers['Cache-Control'] = 'public, max-age=31536000'
        return response

    @app.route('/')
    def landing():
        from models.user import User
        from models.job import JobPosting
        from models.company import Company

        user = None
        user_id = session.get('user_id')
        if user_id:
            user = User.query.get(user_id)

        recent_jobs = JobPosting.query.all()
        if len(recent_jobs) > 6:
            recent_jobs = recent_jobs[:6]

        companies = Company.query.all()[:8]

        return render_template('landing.html', user=user, recent_jobs=recent_jobs, companies=companies)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)