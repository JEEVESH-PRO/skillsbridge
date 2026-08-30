from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db
from models.user import User
from models.company import Company
from database.firestore_db import get_db

auth_bp = Blueprint('auth', __name__)


def _next_id(collection):
    db = get_db()
    return str(len(list(db.collection(collection).stream())) + 1)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['user_id'] = str(user.id)
            session['user_name'] = user.name
            session['user_role'] = user.role
            flash(f'Welcome back, {user.name}!', 'success')
            if user.role == 'employer':
                return redirect(url_for('employer.dashboard'))
            return redirect(url_for('candidate.jobs'))
        else:
            flash('Invalid email or password.', 'error')
    return render_template('auth/login.html')


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    companies = Company.query.all()
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        role = request.form.get('role', 'candidate').strip()
        headline = request.form.get('headline', '').strip()
        company_id = request.form.get('company_id')

        if not name or not email or not password:
            flash('Please fill in all required fields.', 'error')
            return render_template('auth/signup.html', companies=companies)

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('An account with this email already exists.', 'error')
            return render_template('auth/signup.html', companies=companies)

        user_id = _next_id('users')
        user = User(
            id=user_id,
            name=name, email=email, role=role,
            headline=headline or ('Job Candidate' if role == 'candidate' else 'Hiring Manager'),
            company_id=str(company_id) if role == 'employer' and company_id else None
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        session['user_id'] = str(user.id)
        session['user_name'] = user.name
        session['user_role'] = user.role
        flash('Account created successfully!', 'success')

        if user.role == 'employer':
            return redirect(url_for('employer.dashboard'))
        return redirect(url_for('candidate.profile'))
    return render_template('auth/signup.html', companies=companies)


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('auth.login'))
