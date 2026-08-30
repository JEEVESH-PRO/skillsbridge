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
from ml.resume_parser import auto_update_candidate_skills, extract_text_from_file

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
        flash('Please login to access your skills profile.', 'info')
        return redirect(url_for('auth.login'))

    all_skills = Skill.query.all()
    all_skills = sorted(all_skills, key=lambda s: (s.name or '').lower())

    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'update_profile':
            user.name = request.form.get('name', user.name).strip()
            user.headline = request.form.get('headline', user.headline).strip()
            user.bio = request.form.get('bio', user.bio).strip()
            db.session.commit()
            flash('Profile details updated successfully!', 'success')

        elif action == 'add_skill':
            skill_id = request.form.get('skill_id')
            proficiency = request.form.get('proficiency', 'Intermediate')
            
            if skill_id:
                existing = CandidateSkill.query.filter_by(user_id=str(user.id), skill_id=str(skill_id)).first()
                if not existing:
                    cs_id = f"cs_{user.id}_{skill_id}"
                    cs = CandidateSkill(id=cs_id, user_id=str(user.id), skill_id=str(skill_id), proficiency=proficiency)
                    db.session.add(cs)
                    db.session.commit()
                    flash('New skill added to your matrix!', 'success')
                else:
                    existing.proficiency = proficiency
                    db.session.commit()
                    flash('Skill proficiency level updated!', 'info')

        elif action == 'delete_skill':
            candidate_skill_id = request.form.get('candidate_skill_id')
            if candidate_skill_id:
                cs = CandidateSkill.query.get(candidate_skill_id)
                if cs and str(cs.user_id) == str(user.id):
                    db.session.delete(cs)
                    db.session.commit()
                    flash('Skill removed from matrix.', 'info')

        return redirect(url_for('candidate.profile'))

    user_skills = CandidateSkill.query.filter_by(user_id=str(user.id)).all()
    user_skill_ids = [cs.skill_id for cs in user_skills]

    return render_template(
        'candidate/profile.html',
        user=user,
        user_skills=user_skills,
        all_skills=all_skills,
        user_skill_ids=user_skill_ids
    )

@candidate_bp.route('/profile/parse_resume', methods=['POST'])
def parse_resume():
    user = get_current_user()
    if not user:
        flash('Authentication required.', 'error')
        return redirect(url_for('auth.login'))

    resume_text = request.form.get('resume_text', '')
    
    # Handle uploaded resume file (.txt, .pdf, .docx)
    if 'resume_file' in request.files:
        file = request.files['resume_file']
        if file and file.filename:
            extracted_file_text = extract_text_from_file(file)
            resume_text += "\n" + extracted_file_text

    if not resume_text.strip():
        flash('Please paste resume text or upload a PDF/Word/TXT document to extract skills.', 'error')
        return redirect(url_for('candidate.profile'))

    updated_skills = auto_update_candidate_skills(user.id, resume_text)
    
    if updated_skills:
        flash(f'🤖 AI Resume Analyzer extracted {len(updated_skills)} skills: {", ".join(updated_skills)}!', 'success')
    else:
        flash('AI analysis complete. No new skills detected beyond your current matrix.', 'info')

    return redirect(url_for('candidate.profile'))

@candidate_bp.route('/jobs')
def jobs():
    user = get_current_user()
    if not user:
        flash('Please sign in to browse active job openings.', 'info')
        return redirect(url_for('auth.login'))

    domain_filter = request.args.get('domain', '').strip()
    search_query = request.args.get('q', '').strip()

    all_jobs = JobPosting.query.all()
    all_jobs.sort(key=lambda j: j.created_at or '', reverse=True)

    if domain_filter and domain_filter != 'All':
        all_jobs = [j for j in all_jobs if domain_filter.lower() in (j.domain or '').lower()]

    if search_query:
        sq = search_query.lower()
        all_jobs = [j for j in all_jobs if sq in (j.title or '').lower() or sq in (j.domain or '').lower() or sq in (j.description or '').lower()]

    match_scores = {}
    for job in all_jobs:
        analysis = analyze_skill_gap(user, job)
        match_scores[job.id] = {'score': analysis['match_score'], 'status': 'matched' if analysis['match_score'] >= 70 else 'partial'}

    domains = ['All', 'Product-Based IT', 'Service-Based IT', 'AI / Machine Learning', 'Backend Engineering', 'Frontend Engineering', 'DevOps & Cloud', 'Software Development']

    return render_template(
        'candidate/jobs.html',
        jobs=all_jobs,
        domains=domains,
        selected_domain=domain_filter or 'All',
        search_query=search_query,
        match_scores=match_scores,
        user=user
    )

@candidate_bp.route('/jobs/<job_id>')
def job_detail(job_id):
    user = get_current_user()
    if not user:
        flash('Please sign in to view job details.', 'info')
        return redirect(url_for('auth.login'))

    job = JobPosting.query.get_or_404(job_id)
    analysis = analyze_skill_gap(user, job)

    already_applied = False
    if user:
        apps = Application.query.filter_by(user_id=str(user.id), job_id=str(job.id)).all()
        if apps:
            already_applied = True

    return render_template(
        'candidate/job_detail.html',
        job=job,
        analysis=analysis,
        already_applied=already_applied,
        user=user
    )

@candidate_bp.route('/jobs/<job_id>/skills')
def skills_gap(job_id):
    user = get_current_user()
    if not user:
        flash('Please sign in to access skill gap analysis.', 'info')
        return redirect(url_for('auth.login'))

    job = JobPosting.query.get_or_404(job_id)
    analysis = analyze_skill_gap(user, job)

    return render_template(
        'candidate/skills_gap.html',
        job=job,
        analysis=analysis,
        user=user
    )

@candidate_bp.route('/jobs/<job_id>/interview')
def interview(job_id):
    user = get_current_user()
    if not user:
        flash('Please sign in to access interview prep guides.', 'info')
        return redirect(url_for('auth.login'))

    job = JobPosting.query.get_or_404(job_id)
    resources = InterviewResource.query.filter_by(company_id=str(job.company_id)).all()

    return render_template(
        'candidate/interview.html',
        job=job,
        resources=resources,
        user=user
    )

@candidate_bp.route('/jobs/<job_id>/apply', methods=['POST'])
def apply_job(job_id):
    user = get_current_user()
    if not user or not user.is_candidate():
        flash('Please login as a Candidate to apply for jobs.', 'error')
        return redirect(url_for('auth.login'))

    job = JobPosting.query.get_or_404(job_id)
    
    existing = Application.query.filter_by(user_id=str(user.id), job_id=str(job.id)).all()
    if existing:
        flash('You have already applied for this job posting.', 'info')
        return redirect(url_for('candidate.applications'))

    analysis = analyze_skill_gap(user, job)
    
    app_id = f"app_{user.id}_{job.id}"
    app = Application(
        id=app_id,
        user_id=str(user.id),
        job_id=str(job.id),
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

    user_apps = Application.query.filter_by(user_id=str(user.id)).all()
    user_apps.sort(key=lambda a: a.applied_at or '', reverse=True)

    return render_template(
        'candidate/applications.html',
        applications=user_apps,
        user=user
    )

@candidate_bp.route('/learning')
def learning():
    user = get_current_user()
    if not user:
        flash('Please login to view your learning hub.', 'info')
        return redirect(url_for('auth.login'))

    user_skill_ids = [cs.skill_id for cs in user.candidate_skills]
    
    all_courses = Course.query.all()
    recommended_courses = [c for c in all_courses if c.skill_id not in user_skill_ids]
    company_courses = [c for c in all_courses if c.employer_id]

    return render_template(
        'candidate/learning.html',
        courses=recommended_courses,
        company_courses=company_courses,
        user=user
    )
