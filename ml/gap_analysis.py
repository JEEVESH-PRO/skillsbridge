from models.skill import CandidateSkill, Skill
from models.job import JobSkillRequirement
from models.course import Course

PROFICIENCY_WEIGHTS = {
    'Expert': 1.0,
    'Advanced': 0.9,
    'Intermediate': 0.75,
    'Beginner': 0.5
}

def analyze_skill_gap(user, job):
    if not job:
        return {
            'match_score': 0,
            'matched_skills': [],
            'missing_skills': [],
            'summary': 'Job not found.'
        }

    user_skill_map = {}
    if user and user.is_candidate():
        for cs in user.candidate_skills:
            user_skill_map[cs.skill_id] = {
                'skill_name': cs.skill.name,
                'proficiency': cs.proficiency,
                'weight': PROFICIENCY_WEIGHTS.get(cs.proficiency, 0.75)
            }

    job_requirements = job.skill_requirements
    if not job_requirements:
        return {
            'match_score': 100,
            'matched_skills': [],
            'missing_skills': [],
            'summary': 'No specific skill requirements listed for this job.'
        }

    matched_skills = []
    missing_skills = []
    total_weighted_match = 0.0

    for req in job_requirements:
        sk_id = req.skill_id
        sk_name = req.skill.name if req.skill else "Unknown Skill"
        req_lvl = req.required_level or 'Intermediate'
        req_weight = PROFICIENCY_WEIGHTS.get(req_lvl, 0.75)

        if sk_id in user_skill_map:
            u_sk = user_skill_map[sk_id]
            u_weight = u_sk['weight']
            
            skill_score = min(1.0, u_weight / max(0.1, req_weight))
            total_weighted_match += skill_score

            matched_skills.append({
                'skill_id': sk_id,
                'name': sk_name,
                'user_level': u_sk['proficiency'],
                'required_level': req_lvl,
                'status': 'Matched' if skill_score >= 0.85 else 'Partial Match'
            })
        else:
            courses = Course.query.filter_by(skill_id=sk_id).limit(3).all()
            course_list = []
            for c in courses:
                course_list.append({
                    'id': c.id,
                    'title': c.title,
                    'provider': c.provider,
                    'source_type': c.source_type,
                    'url': c.url,
                    'duration': c.duration,
                    'difficulty': c.difficulty
                })

            missing_skills.append({
                'skill_id': sk_id,
                'name': sk_name,
                'required_level': req_lvl,
                'gap_severity': 'High' if req_lvl in ['Advanced', 'Expert'] else 'Medium',
                'courses': course_list
            })

    total_req_count = len(job_requirements)
    match_score = int(round((total_weighted_match / total_req_count) * 100))
    match_score = min(100, max(0, match_score))

    if match_score >= 85:
        summary = f"Strong Match ({match_score}%)! You meet almost all required skill criteria for {job.title}."
    elif match_score >= 50:
        missing_names = ", ".join([s['name'] for s in missing_skills[:2]])
        summary = f"Moderate Match ({match_score}%). Upskilling in {missing_names or 'missing areas'} will make your application stand out."
    else:
        summary = f"Skill Gap Identified ({match_score}% Match). Follow the recommended courses below to bridge your skill gap."

    return {
        'match_score': match_score,
        'total_required': total_req_count,
        'matched_count': len(matched_skills),
        'missing_count': len(missing_skills),
        'matched_skills': matched_skills,
        'missing_skills': missing_skills,
        'summary': summary
    }
