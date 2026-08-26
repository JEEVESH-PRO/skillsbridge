from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db
from models.company import Company
from models.job import JobPosting
from models.user import User

company_bp = Blueprint('company', __name__)

def get_current_user():
    user_id = session.get('user_id')
    if user_id:
        return User.query.get(user_id)
    return None

@company_bp.route('/companies')
def company_list():
    query = request.args.get('q', '').strip()
    if query:
        companies = Company.query.filter(
            (Company.name.ilike(f"%{query}%")) |
            (Company.industry.ilike(f"%{query}%")) |
            (Company.location.ilike(f"%{query}%"))
        ).all()
    else:
        companies = Company.query.all()

    user = get_current_user()
    return render_template('company/list.html', companies=companies, query=query, user=user)

@company_bp.route('/companies/<name>')
def company_detail(name):
    company = Company.query.filter(Company.name.ilike(name)).first_or_404()
    jobs = JobPosting.query.filter_by(company_id=company.id).order_by(JobPosting.created_at.desc()).all()
    user = get_current_user()

    return render_template(
        'company/detail.html',
        company=company,
        jobs=jobs,
        user=user
    )
