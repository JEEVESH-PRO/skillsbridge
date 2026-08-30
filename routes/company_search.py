from flask import Blueprint, render_template, request, session, redirect, url_for, flash
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
    user = get_current_user()
    if not user:
        flash('Please sign in to browse companies.', 'info')
        return redirect(url_for('auth.login'))

    category_filter = request.args.get('category', '').strip()
    search_query = request.args.get('q', '').strip()

    companies = Company.query.all()
    companies.sort(key=lambda c: (c.name or '').lower())

    if category_filter and category_filter != 'All':
        companies = [c for c in companies if category_filter.lower() in (c.industry or '').lower()]

    if search_query:
        sq = search_query.lower()
        companies = [c for c in companies if sq in (c.name or '').lower() or sq in (c.industry or '').lower() or sq in (c.location or '').lower()]

    categories = ['All', 'Product-Based IT', 'Service-Based IT', 'AI & DeepTech', 'Fintech', 'Hardware & Semiconductors']

    return render_template(
        'company/list.html',
        companies=companies,
        categories=categories,
        selected_category=category_filter or 'All',
        search_query=search_query,
        user=user
    )

@company_bp.route('/companies/<name>')
def company_detail(name):
    user = get_current_user()
    if not user:
        flash('Please sign in to view company details.', 'info')
        return redirect(url_for('auth.login'))

    comp_matches = Company.query.filter_by(name=name).all()
    if not comp_matches:
        comp_matches = [c for c in Company.query.all() if (c.name or '').lower() == name.lower()]

    if not comp_matches:
        flash('Company not found.', 'error')
        return redirect(url_for('company.company_list'))

    company = comp_matches[0]
    company_jobs = JobPosting.query.filter_by(company_id=str(company.id)).all()

    return render_template(
        'company/detail.html',
        company=company,
        jobs=company_jobs,
        user=user
    )
