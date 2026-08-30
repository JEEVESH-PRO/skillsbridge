import re
import io
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
    'c#': ('C#', 'Programming Languages'),
    'csharp': ('C#', 'Programming Languages'),
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
    'html': ('HTML5', 'Frontend'),
    'css': ('CSS3', 'Frontend'),
    'tailwind': ('Tailwind CSS', 'Frontend'),
    'bootstrap': ('Bootstrap', 'Frontend'),

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
    'pandas': ('Pandas', 'Data Science'),
    'numpy': ('NumPy', 'Data Science'),

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
    'github': ('Git', 'Tools'),
    'ui/ux': ('UI/UX Design', 'Design'),
    'figma': ('UI/UX Design', 'Design')
}

def extract_text_from_file(file_storage):
    """
    Extracts raw text from uploaded PDF, DOCX, or TXT document file objects.
    """
    filename = (file_storage.filename or '').lower()
    file_bytes = file_storage.read()
    text = ""

    if filename.endswith('.pdf'):
        # Extract text from PDF document
        try:
            import pypdf
            reader = pypdf.PdfReader(io.BytesIO(file_bytes))
            for page in reader.pages:
                text += page.extract_text() + "\n"
        except Exception:
            # Fallback regex raw string scanner for PDF streams
            try:
                raw_str = file_bytes.decode('latin-1', errors='ignore')
                text = " ".join(re.findall(r'[a-zA-Z0-9\+\#\.\/]{2,}', raw_str))
            except Exception:
                text = ""

    elif filename.endswith('.docx'):
        # Extract text from Word DOCX document
        try:
            import docx
            doc = docx.Document(io.BytesIO(file_bytes))
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception:
            text = file_bytes.decode('utf-8', errors='ignore')

    else:
        # Plain text file
        text = file_bytes.decode('utf-8', errors='ignore')

    return text

def parse_resume_text(resume_text):
    """
    Real AI Resume Skill Extractor using NLP keyword matching and context analysis.
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
            if count >= 4 or 'lead' in text_lower or 'expert' in text_lower or 'senior' in text_lower or 'architect' in text_lower:
                proficiency = 'Expert'
            elif count >= 2 or 'advanced' in text_lower or 'proficient' in text_lower or '3+ years' in text_lower:
                proficiency = 'Advanced'
            elif 'experienced' in text_lower or 'built' in text_lower or 'project' in text_lower:
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
            sk_id = f"sk_{len(list(Skill.query.all())) + 1}"
            sk = Skill(id=sk_id, name=sk_name, category=sk_cat)
            db.session.add(sk)
            db.session.commit()

        # Get or create CandidateSkill
        cs = CandidateSkill.query.filter_by(user_id=str(user_id), skill_id=str(sk.id)).first()
        if not cs:
            cs_id = f"cs_{user_id}_{sk.id}"
            cs = CandidateSkill(id=cs_id, user_id=str(user_id), skill_id=str(sk.id), proficiency=prof)
            db.session.add(cs)
            updated_skills.append(f"{sk_name} ({prof})")
        else:
            order = {'Beginner': 1, 'Intermediate': 2, 'Advanced': 3, 'Expert': 4}
            if order.get(prof, 2) > order.get(cs.proficiency, 2):
                cs.proficiency = prof
                updated_skills.append(f"{sk_name} ({prof})")
    
    db.session.commit()
    return updated_skills
