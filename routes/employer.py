from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db
from models.user import User
from models.company import Company
from models.job import JobPosting, JobSkillRequirement
from models.skill import Skill
from models.application import Application
from models.course import Course
from database.firestore_db import get_db

employer_bp = Blueprint('employer', __name__)


def get_current_employer():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        if user and user.is_employer():
            return user
    return None


def _next_id(collection):
    db = get_db()
    return str(len(list(db.collection(collection).stream())) + 1)


@employer_bp.route('/employer/dashboard')
def dashboard():
    user = get_current_employer()
    if not user:
        flash('Employer access required. Please login as an Employer.', 'error')
        return redirect(url_for('auth.login'))

    company = user.employer_company
    if not company:
        company = Company.query.first()
        if company:
            user.company_id = company.id
            db.session.commit()

    jobs = JobPosting.query.filter_by(company_id=str(company.id)).all() if company else []
    jobs.sort(key=lambda j: j.created_at or '', reverse=True)

    total_applicants = 0
    shortlisted_count = 0
    job_stats = []

    for job in jobs:
        apps = Application.query.filter_by(job_id=str(job.id)).all()
        app_cnt = len(apps)
        shortlisted_cnt = sum(1 for a in apps if a.status == 'Shortlisted')
        total_applicants += app_cnt
        shortlisted_count += shortlisted_cnt

        job_stats.append({
            'job': job,
            'applicant_count': app_cnt,
            'shortlisted_count': shortlisted_cnt
        })

    return render_template(
        'employer/dashboard.html', user=user, company=company,
        job_stats=job_stats, total_jobs=len(jobs),
        total_applicants=total_applicants, shortlisted_count=shortlisted_count,
    )


@employer_bp.route('/employer/jobs/new', methods=['GET', 'POST'])
def post_job():
    user = get_current_employer()
    if not user:
        flash('Employer access required.', 'error')
        return redirect(url_for('auth.login'))

    all_skills = Skill.query.all()
    all_skills = sorted(all_skills, key=lambda s: (s.name or '').lower())

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        domain = request.form.get('domain', 'Software Development').strip()
        experience_required = request.form.get('experience_required', '1-3 yrs').strip()
        location = request.form.get('location', 'Remote').strip()
        salary_range = request.form.get('salary_range', '$100k - $140k').strip()
        description = request.form.get('description', '').strip()
        selected_skill_ids = request.form.getlist('skill_ids')

        if not title or not description:
            flash('Please provide a job title and description.', 'error')
            return render_template('employer/post_job.html', user=user, skills=all_skills)

        job = JobPosting(
            id=_next_id('job_postings'),
            company_id=str(user.company_id or '1'), title=title, domain=domain,
            experience_required=experience_required, location=location,
            salary_range=salary_range, description=description,
        )
        db.session.add(job)
        db.session.commit()

        for sk_id in selected_skill_ids:
            req = JobSkillRequirement(
                id=f"{job.id}_{sk_id}", job_id=job.id,
                skill_id=str(sk_id), required_level='Intermediate',
            )
            db.session.add(req)
        db.session.commit()

        flash(f'Job posting "{title}" created successfully!', 'success')
        return redirect(url_for('employer.dashboard'))

    return render_template('employer/post_job.html', user=user, skills=all_skills)


@employer_bp.route('/employer/jobs/<job_id>/applicants')
def view_applicants(job_id):
    user = get_current_employer()
    if not user:
        flash('Employer access required.', 'error')
        return redirect(url_for('auth.login'))

    job = JobPosting.query.get_or_404(job_id)
    applications = Application.query.filter_by(job_id=str(job.id)).all()
    applications.sort(key=lambda a: a.match_score or 0, reverse=True)

    return render_template('employer/applicants.html', user=user, job=job, applications=applications)


@employer_bp.route('/employer/applications/<app_id>/status', methods=['POST'])
def update_application_status(app_id):
    user = get_current_employer()
    if not user:
        flash('Employer access required.', 'error')
        return redirect(url_for('auth.login'))

    application = Application.query.get_or_404(app_id)
    new_status = request.form.get('status', 'Applied')

    if new_status in ['Applied', 'Shortlisted', 'Rejected']:
        application.status = new_status
        db.session.commit()
        flash(f'Candidate application updated to {new_status}.', 'success')

    return redirect(url_for('employer.view_applicants', job_id=application.job_id))


@employer_bp.route('/employer/courses/new', methods=['GET', 'POST'])
def new_course():
    user = get_current_employer()
    if not user:
        flash('Employer access required.', 'error')
        return redirect(url_for('auth.login'))

    all_skills = Skill.query.all()
    all_skills = sorted(all_skills, key=lambda s: (s.name or '').lower())

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        skill_id = request.form.get('skill_id')
        source_type = request.form.get('source_type', 'company')
        url = request.form.get('url', '').strip()
        duration = request.form.get('duration', '3 Weeks')
        difficulty = request.form.get('difficulty', 'Intermediate')

        if not title or not url or not skill_id:
            flash('Please fill in all course fields.', 'error')
            return render_template('employer/new_course.html', user=user, skills=all_skills)

        course = Course(
            id=_next_id('courses'), skill_id=str(skill_id), title=title,
            provider=user.employer_company.name if user.employer_company else 'Employer Partner',
            source_type=source_type, url=url, duration=duration,
            difficulty=difficulty, employer_id=str(user.id),
        )
        db.session.add(course)
        db.session.commit()

        flash(f'Course "{title}" added to skill training catalog!', 'success')
        return redirect(url_for('employer.dashboard'))

    return render_template('employer/new_course.html', user=user, skills=all_skills)
