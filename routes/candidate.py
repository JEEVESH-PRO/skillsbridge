from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from models import db
from models.user import User
from models.job import JobPosting
from models.company import Company
from models.skill import Skill, CandidateSkill
from models.application import Application
from models.course import Course
from models.interview_resource import InterviewResource
from ml.gap_analysis import analyze_skill_gap

candidate_bp = Blueprint('candidate', __name__)

def get_current_user():
    user_id = session.get('user_id')
    if user_id:
        return User.query.get(user_id)
    return None

@candidate_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    user = get_current_user()
    if not user:
        flash('Please login to access your profile.', 'info')
        return redirect(url_for('auth.login'))

    all_skills = Skill.query.order_by(Skill.name).all()

    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'update_profile':
            user.name = request.form.get('name', user.name).strip()
            user.headline = request.form.get('headline', user.headline).strip()
            user.bio = request.form.get('bio', user.bio).strip()
            db.session.commit()
            flash('Profile details updated!', 'success')

        elif action == 'add_skill':
            skill_id = request.form.get('skill_id')
            proficiency = request.form.get('proficiency', 'Intermediate')
            
            if skill_id:
                existing = CandidateSkill.query.filter_by(user_id=user.id, skill_id=int(skill_id)).first()
                if not existing:
                    cs = CandidateSkill(user_id=user.id, skill_id=int(skill_id), proficiency=proficiency)
                    db.session.add(cs)
                    db.session.commit()
                    flash('Skill added to profile!', 'success')
                else:
                    existing.proficiency = proficiency
                    db.session.commit()
                    flash('Skill proficiency updated!', 'info')

        elif action == 'delete_skill':
            candidate_skill_id = request.form.get('candidate_skill_id')
            if candidate_skill_id:
                cs = CandidateSkill.query.filter_by(id=int(candidate_skill_id), user_id=user.id).first()
                if cs:
                    db.session.delete(cs)
                    db.session.commit()
                    flash('Skill removed from profile.', 'info')

        return redirect(url_for('candidate.profile'))

    user_skills = CandidateSkill.query.filter_by(user_id=user.id).all()
    user_skill_ids = [cs.skill_id for cs in user_skills]

    return render_template(
        'candidate/profile.html',
        user=user,
        user_skills=user_skills,
        all_skills=all_skills,
        user_skill_ids=user_skill_ids
    )

@candidate_bp.route('/jobs')
def jobs():
    user = get_current_user()
    domain_filter = request.args.get('domain', '').strip()
    search_query = request.args.get('q', '').strip()

    query = JobPosting.query.join(Company)

    if domain_filter and domain_filter != 'All':
        query = query.filter(JobPosting.domain.ilike(f"%{domain_filter}%"))

    if search_query:
        query = query.filter(
            (JobPosting.title.ilike(f"%{search_query}%")) |
            (Company.name.ilike(f"%{search_query}%")) |
            (JobPosting.description.ilike(f"%{search_query}%"))
        )

    all_jobs = query.order_by(JobPosting.created_at.desc()).all()

    # Calculate match percentage preview for candidate
    match_scores = {}
    for job in all_jobs:
        analysis = analyze_skill_gap(user, job)
        match_scores[job.id] = {'score': analysis['match_score'], 'status': 'matched' if analysis['match_score'] >= 70 else 'partial'}

    domains = ['All', 'Backend Engineering', 'AI / Machine Learning', 'Frontend Engineering', 'DevOps & Cloud', 'Software Development']

    return render_template(
        'candidate/jobs.html',
        jobs=all_jobs,
        domains=domains,
        selected_domain=domain_filter or 'All',
        search_query=search_query,
        match_scores=match_scores,
        job_match_map={k: v['score'] for k, v in match_scores.items()},
        user=user
    )

@candidate_bp.route('/jobs/<int:job_id>')
def job_detail(job_id):
    user = get_current_user()
    job = JobPosting.query.get_or_404(job_id)
    analysis = analyze_skill_gap(user, job)

    already_applied = False
    if user:
        app = Application.query.filter_by(user_id=user.id, job_id=job.id).first()
        if app:
            already_applied = True

    return render_template(
        'candidate/job_detail.html',
        job=job,
        analysis=analysis,
        already_applied=already_applied,
        user=user
    )

@candidate_bp.route('/jobs/<int:job_id>/skills')
def skills_gap(job_id):
    user = get_current_user()
    job = JobPosting.query.get_or_404(job_id)
    analysis = analyze_skill_gap(user, job)

    return render_template(
        'candidate/skills_gap.html',
        job=job,
        analysis=analysis,
        user=user
    )

@candidate_bp.route('/jobs/<int:job_id>/interview')
def interview(job_id):
    user = get_current_user()
    job = JobPosting.query.get_or_404(job_id)
    
    # Fetch interview resources for company and optionally job
    resources = InterviewResource.query.filter(
        (InterviewResource.company_id == job.company_id)
    ).all()

    return render_template(
        'candidate/interview.html',
        job=job,
        resources=resources,
        user=user
    )

@candidate_bp.route('/jobs/<int:job_id>/apply', methods=['POST'])
def apply_job(job_id):
    user = get_current_user()
    if not user or not user.is_candidate():
        flash('Please login as a Candidate to apply for jobs.', 'error')
        return redirect(url_for('auth.login'))

    job = JobPosting.query.get_or_404(job_id)
    
    existing = Application.query.filter_by(user_id=user.id, job_id=job.id).first()
    if existing:
        flash('You have already applied for this job posting.', 'info')
        return redirect(url_for('candidate.applications'))

    analysis = analyze_skill_gap(user, job)
    
    app = Application(
        user_id=user.id,
        job_id=job.id,
        status='Applied',
        match_score=analysis['match_score']
    )
    db.session.add(app)
    db.session.commit()

    flash(f'Application submitted successfully for {job.title}! (Skill Match: {analysis["match_score"]}%)', 'success')
    return redirect(url_for('candidate.applications'))

@candidate_bp.route('/applications')
def applications():
    user = get_current_user()
    if not user:
        flash('Please login to view your applications.', 'info')
        return redirect(url_for('auth.login'))

    user_apps = Application.query.filter_by(user_id=user.id).order_by(Application.applied_at.desc()).all()

    return render_template(
        'candidate/applications.html',
        applications=user_apps,
        user=user
    )

@candidate_bp.route('/learning')
def learning():
    user = get_current_user()
    if not user:
        flash('Please login to view your learning resources.', 'info')
        return redirect(url_for('auth.login'))

    # Collect missing skills across all jobs or user profile
    user_skill_ids = [cs.skill_id for cs in user.candidate_skills]
    
    # Recommend courses for skills the candidate DOES NOT possess yet
    recommended_courses = Course.query.filter(~Course.skill_id.in_(user_skill_ids if user_skill_ids else [-1])).all()

    # Also list employer-offered courses
    company_courses = Course.query.filter(Course.employer_id.isnot(None)).all()

    return render_template(
        'candidate/learning.html',
        courses=recommended_courses,
        company_courses=company_courses,
        user=user
    )
