import os
from flask import Flask, render_template, session, url_for
from config import Config
from database.firestore_db import init_firestore
from database.seed_data import seed_database

from routes.auth import auth_bp
from routes.candidate import candidate_bp
from routes.company_search import company_bp
from routes.employer import employer_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    init_firestore()

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

        featured_companies = Company.query.limit(5).all()
        recent_jobs = JobPosting.query.all()[:4]

        return render_template('landing.html', user=user, companies=featured_companies, recent_jobs=recent_jobs)

    seed_database()

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)
