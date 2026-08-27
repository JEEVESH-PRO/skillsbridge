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
    companies = Company.query.all()

    if query:
        q = query.lower()
        companies = [
            c for c in companies
            if q in (c.name or '').lower()
            or q in (c.industry or '').lower()
            or q in (c.location or '').lower()
        ]

    companies = sorted(companies, key=lambda c: (c.name or '').lower())

    user = get_current_user()
    return render_template('company/list.html', companies=companies, query=query, user=user)


@company_bp.route('/companies/<name>')
def company_detail(name):
    companies = Company.query.all()
    company = next((c for c in companies if (c.name or '').lower() == name.lower()), None)
    if not company:
        from flask import abort
        abort(404)

    jobs = JobPosting.query.filter_by(company_id=str(company.id)).all()
    jobs.sort(key=lambda j: j.created_at or '', reverse=True)

    user = get_current_user()

    return render_template(
        'company/detail.html',
        company=company,
        jobs=jobs,
        user=user
    )
