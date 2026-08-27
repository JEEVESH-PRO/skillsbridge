import os
import uuid
import tempfile
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db
from models.user import User
from models.job import JobPosting
from models.company import Company
from models.skill import Skill, CandidateSkill
from models.application import Application
from models.course import Course
from models.interview_resource import InterviewResource
from ml.gap_analysis import analyze_skill_gap
from functions.resume_parser import extract_skills_from_resume, match_resume_skills_to_db
from database.firestore_db import get_db

candidate_bp = Blueprint('candidate', __name__)

# Netlify function filesystems are read-only except /tmp, so store uploads in a temp dir.
UPLOAD_FOLDER = tempfile.gettempdir()
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'txt'}


def get_current_user():
    user_id = session.get('user_id')
    if user_id:
        return User.query.get(user_id)
    return None


def _next_id(collection):
    db = get_db()
    return str(len(list(db.collection(collection).stream())) + 1)


@candidate_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    user = get_current_user()
    if not user:
        flash('Please login to access your profile.', 'info')
        return redirect(url_for('auth.login'))

    all_skills = Skill.query.all()
    # Manual order by name via sort
    all_skills = sorted(all_skills, key=lambda s: (s.name or '').lower())

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'update_profile':
            user.name = request.form.get('name', user.name).strip()
            user.headline = request.form.get('headline', user.headline).strip()
            user.bio = request.form.get('bio', user.bio).strip()
            db.session.commit()
            flash('Profile details updated!', 'success')

        elif action == 'add_skill':
            skill_id = str(request.form.get('skill_id')).strip()
            proficiency = request.form.get('proficiency', 'Intermediate')

            if skill_id:
                existing = CandidateSkill.query.filter_by(user_id=str(user.id), skill_id=skill_id).first()
                if not existing:
                    cs = CandidateSkill(id=_next_id('candidate_skills'), user_id=str(user.id), skill_id=skill_id, proficiency=proficiency)
                    db.session.add(cs)
                    db.session.commit()
                    flash('Skill added to profile!', 'success')
                else:
                    existing.proficiency = proficiency
                    db.session.commit()
                    flash('Skill proficiency updated!', 'info')

        elif action == 'delete_skill':
            candidate_skill_id = str(request.form.get('candidate_skill_id')).strip()
            if candidate_skill_id:
                cs = CandidateSkill.query.filter_by(id=candidate_skill_id, user_id=str(user.id)).first()
                if cs:
                    db.session.delete(cs)
                    db.session.commit()
                    flash('Skill removed from profile.', 'info')

        return redirect(url_for('candidate.profile'))

    user_skills = CandidateSkill.query.filter_by(user_id=str(user.id)).all()
    user_skill_ids = [cs.skill_id for cs in user_skills]

    return render_template(
        'candidate/profile.html',
        user=user, user_skills=user_skills,
        all_skills=all_skills, user_skill_ids=user_skill_ids,
    )


@candidate_bp.route('/profile/upload-resume', methods=['POST'])
def upload_resume():
    user = get_current_user()
    if not user:
        flash('Please login to upload a resume.', 'info')
        return redirect(url_for('auth.login'))

    if 'resume' not in request.files:
        flash('No file selected. Please choose a resume file.', 'error')
        return redirect(url_for('candidate.profile'))

    file = request.files['resume']
    if file.filename == '':
        flash('No file selected. Please choose a resume file.', 'error')
        return redirect(url_for('candidate.profile'))

    file_ext = file.filename.rsplit('.', 1)[-1].lower() if '.' in file.filename else ''
    if file_ext not in ALLOWED_EXTENSIONS:
        flash('Invalid file type. Please upload PDF, DOCX, DOC, or TXT files.', 'error')
        return redirect(url_for('candidate.profile'))

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    filename = f"{uuid.uuid4().hex}_{file.filename}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    detected_skills, _ = extract_skills_from_resume(filepath)
    try:
        os.remove(filepath)
    except Exception:
        pass

    if not detected_skills:
        flash('Could not detect any known skills from your resume. Try adding skills manually.', 'error')
        return redirect(url_for('candidate.profile'))

    all_db_skills = Skill.query.all()
    matched_skills = match_resume_skills_to_db(detected_skills, all_db_skills)

    added_count = 0
    for skill in matched_skills:
        sid = str(skill.id)
        existing = CandidateSkill.query.filter_by(user_id=str(user.id), skill_id=sid).first()
        if not existing:
            cs = CandidateSkill(id=_next_id('candidate_skills'), user_id=str(user.id), skill_id=sid, proficiency='Intermediate')
            db.session.add(cs)
            added_count += 1

    db.session.commit()

    unmatched = [s for s in detected_skills if s not in [ms.name for ms in matched_skills]]
    msg = f'Resume analyzed! Added {added_count} new skill(s) to your profile.'
    if unmatched:
        msg += f' Could not match: {", ".join(unmatched)}.'
    flash(msg, 'success')
    return redirect(url_for('candidate.profile'))


@candidate_bp.route('/jobs')
def jobs():
    user = get_current_user()
    domain_filter = request.args.get('domain', '').strip()
    search_query = request.args.get('q', '').strip()

    all_jobs = JobPosting.query.all()

    if domain_filter and domain_filter != 'All':
        all_jobs = [j for j in all_jobs if domain_filter.lower() in (j.domain or '').lower()]
    if search_query:
        q = search_query.lower()
        caps = [c.name.lower() for c in Company.query.all()]
        all_jobs = [
            j for j in all_jobs
            if q in (j.title or '').lower() or q in (j.description or '').lower()
        ]

    all_jobs.sort(key=lambda j: j.created_at or '', reverse=True)

    match_scores = {}
    for job in all_jobs:
        analysis = analyze_skill_gap(user, job)
        match_scores[job.id] = {'score': analysis['match_score'], 'status': 'matched' if analysis['match_score'] >= 70 else 'partial'}

    domains = ['All', 'Backend Engineering', 'AI / Machine Learning', 'Frontend Engineering', 'DevOps & Cloud', 'Software Development']

    return render_template(
        'candidate/jobs.html', jobs=all_jobs, domains=domains,
        selected_domain=domain_filter or 'All', search_query=search_query,
        match_scores=match_scores, job_match_map={k: v['score'] for k, v in match_scores.items()},
        user=user,
    )


@candidate_bp.route('/jobs/<job_id>')
def job_detail(job_id):
    user = get_current_user()
    job = JobPosting.query.get_or_404(job_id)
    analysis = analyze_skill_gap(user, job)

    already_applied = False
    if user:
        app = Application.query.filter_by(user_id=str(user.id), job_id=str(job.id)).first()
        if app:
            already_applied = True

    return render_template('candidate/job_detail.html', job=job, analysis=analysis, already_applied=already_applied, user=user)


@candidate_bp.route('/jobs/<job_id>/skills')
def skills_gap(job_id):
    user = get_current_user()
    job = JobPosting.query.get_or_404(job_id)
    analysis = analyze_skill_gap(user, job)
    return render_template('candidate/skills_gap.html', job=job, analysis=analysis, user=user)


@candidate_bp.route('/jobs/<job_id>/interview')
def interview(job_id):
    user = get_current_user()
    job = JobPosting.query.get_or_404(job_id)
    resources = InterviewResource.query.filter_by(company_id=str(job.company_id)).all()
    return render_template('candidate/interview.html', job=job, resources=resources, user=user)


@candidate_bp.route('/jobs/<job_id>/apply', methods=['POST'])
def apply_job(job_id):
    user = get_current_user()
    if not user or not user.is_candidate():
        flash('Please login as a Candidate to apply.', 'error')
        return redirect(url_for('auth.login'))

    job = JobPosting.query.get_or_404(job_id)
    existing = Application.query.filter_by(user_id=str(user.id), job_id=str(job.id)).first()
    if existing:
        flash('You have already applied for this job.', 'info')
        return redirect(url_for('candidate.applications'))

    analysis = analyze_skill_gap(user, job)
    app = Application(
        id=_next_id('applications'), user_id=str(user.id), job_id=str(job.id),
        status='Applied', match_score=analysis['match_score'],
    )
    db.session.add(app)
    db.session.commit()

    flash(f'Application submitted successfully! Skill Match: {analysis["match_score"]}%', 'success')
    return redirect(url_for('candidate.applications'))


@candidate_bp.route('/applications')
def applications():
    user = get_current_user()
    if not user:
        flash('Please login to view your applications.', 'info')
        return redirect(url_for('auth.login'))

    user_apps = Application.query.filter_by(user_id=str(user.id)).all()
    user_apps.sort(key=lambda a: a.applied_at or '', reverse=True)

    return render_template('candidate/applications.html', applications=user_apps, user=user)


@candidate_bp.route('/learning')
def learning():
    user = get_current_user()
    if not user:
        flash('Please login to view your learning resources.', 'info')
        return redirect(url_for('auth.login'))

    user_skill_ids = [cs.skill_id for cs in user.candidate_skills]
    all_courses = Course.query.all()
    recommended = [c for c in all_courses if c.skill_id not in user_skill_ids] if user_skill_ids else all_courses
    company_courses = [c for c in all_courses if c.employer_id]

    return render_template('candidate/learning.html', courses=recommended, company_courses=company_courses, user=user)
