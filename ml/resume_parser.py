import re
from models import db
from models.skill import Skill, CandidateSkill

# Comprehensive skill keyword map with categories and defaults
SKILL_DICTIONARY = {
    # Programming Languages
    'python': ('Python', 'Programming Languages'),
    'javascript': ('JavaScript', 'Programming Languages'),
    'typescript': ('TypeScript', 'Programming Languages'),
    'java': ('Java', 'Programming Languages'),
    'c++': ('C++', 'Programming Languages'),
    'cpp': ('C++', 'Programming Languages'),
    'golang': ('Go', 'Programming Languages'),
    'go': ('Go', 'Programming Languages'),
    'rust': ('Rust', 'Programming Languages'),
    'sql': ('SQL', 'Database'),
    
    # Web & Frameworks
    'flask': ('Flask', 'Web Development'),
    'django': ('Django', 'Web Development'),
    'react': ('React', 'Frontend'),
    'reactjs': ('React', 'Frontend'),
    'next.js': ('Next.js', 'Frontend'),
    'nextjs': ('Next.js', 'Frontend'),
    'vue': ('Vue.js', 'Frontend'),
    'vuejs': ('Vue.js', 'Frontend'),
    'angular': ('Angular', 'Frontend'),
    'node.js': ('Node.js', 'Backend'),
    'nodejs': ('Node.js', 'Backend'),
    'express': ('Express.js', 'Backend'),
    'fastapi': ('FastAPI', 'Backend'),
    
    # AI / Machine Learning
    'pytorch': ('PyTorch', 'Machine Learning / AI'),
    'tensorflow': ('TensorFlow', 'Machine Learning / AI'),
    'machine learning': ('Machine Learning', 'Machine Learning / AI'),
    'deep learning': ('Deep Learning', 'Machine Learning / AI'),
    'nlp': ('Natural Language Processing', 'Machine Learning / AI'),
    'computer vision': ('Computer Vision', 'Machine Learning / AI'),
    'scikit-learn': ('Scikit-Learn', 'Machine Learning / AI'),
    'sklearn': ('Scikit-Learn', 'Machine Learning / AI'),
    'langchain': ('LangChain', 'Machine Learning / AI'),
    'llm': ('LLM Architectures', 'Machine Learning / AI'),
    
    # DevOps, Cloud & Infra
    'docker': ('Docker', 'DevOps & Cloud'),
    'kubernetes': ('Kubernetes', 'DevOps & Cloud'),
    'k8s': ('Kubernetes', 'DevOps & Cloud'),
    'aws': ('AWS', 'DevOps & Cloud'),
    'azure': ('Azure', 'DevOps & Cloud'),
    'gcp': ('GCP', 'DevOps & Cloud'),
    'terraform': ('Terraform', 'DevOps & Cloud'),
    'ci/cd': ('CI/CD Pipelines', 'DevOps & Cloud'),
    'github actions': ('CI/CD Pipelines', 'DevOps & Cloud'),

    # Databases & Systems
    'postgresql': ('PostgreSQL', 'Database'),
    'postgres': ('PostgreSQL', 'Database'),
    'mongodb': ('MongoDB', 'Database'),
    'redis': ('Redis', 'Database & Caching'),
    'system design': ('System Design', 'Core Computer Science'),
    'dsa': ('Data Structures & Algorithms', 'Core Computer Science'),
    'data structures': ('Data Structures & Algorithms', 'Core Computer Science'),
    'graphql': ('GraphQL', 'API Design'),
    'rest api': ('REST APIs', 'API Design'),
    'git': ('Git', 'Tools'),
    'ui/ux': ('UI/UX Design', 'Design'),
    'figma': ('UI/UX Design', 'Design')
}

def parse_resume_text(resume_text):
    """
    Parses resume text in real time using NLP keyword extraction,
    maps skills against the global dictionary, and estimates proficiency.
    Returns a list of extracted skills: [{'name': ..., 'category': ..., 'proficiency': ...}]
    """
    if not resume_text:
        return []

    text_lower = resume_text.lower()
    extracted_skills = {}

    for keyword, (skill_name, category) in SKILL_DICTIONARY.items():
        pattern = r'\b' + re.escape(keyword) + r'\b'
        matches = re.findall(pattern, text_lower)
        count = len(matches)
        
        if count > 0:
            if count >= 5 or 'lead' in text_lower or 'expert' in text_lower or 'senior' in text_lower:
                proficiency = 'Expert'
            elif count >= 3 or 'advanced' in text_lower or 'proficient' in text_lower:
                proficiency = 'Advanced'
            elif count >= 2 or 'experienced' in text_lower:
                proficiency = 'Intermediate'
            else:
                proficiency = 'Beginner'

            extracted_skills[skill_name] = {
                'name': skill_name,
                'category': category,
                'proficiency': proficiency
            }

    return list(extracted_skills.values())

def auto_update_candidate_skills(user_id, resume_text):
    """
    Parses resume_text and automatically appends newly extracted skills to the candidate's skill matrix.
    """
    extracted = parse_resume_text(resume_text)
    if not extracted:
        return []

    updated_skills = []
    for item in extracted:
        sk_name = item['name']
        sk_cat = item['category']
        prof = item['proficiency']

        # Get or create Skill
        sk = Skill.query.filter_by(name=sk_name).first()
        if not sk:
            sk_id = str(len(list(Skill.query.all())) + 1)
            sk = Skill(id=sk_id, name=sk_name, category=sk_cat)
            db.session.add(sk)
            db.session.commit()

        # Get or create CandidateSkill
        cs = CandidateSkill.query.filter_by(user_id=str(user_id), skill_id=str(sk.id)).first()
        if not cs:
            cs_id = f"{user_id}_{sk.id}"
            cs = CandidateSkill(id=cs_id, user_id=str(user_id), skill_id=str(sk.id), proficiency=prof)
            db.session.add(cs)
            updated_skills.append(sk_name)
        else:
            order = {'Beginner': 1, 'Intermediate': 2, 'Advanced': 3, 'Expert': 4}
            if order.get(prof, 2) > order.get(cs.proficiency, 2):
                cs.proficiency = prof
                updated_skills.append(sk_name)
    
    db.session.commit()
    return updated_skills
