import os
import re

KNOWN_SKILLS = {
    'python': 'Python',
    'java': 'JavaScript',
    'javascript': 'JavaScript',
    'typescript': 'TypeScript',
    'react': 'React',
    'reactjs': 'React',
    'react.js': 'React',
    'node': 'Node.js',
    'nodejs': 'Node.js',
    'node.js': 'Node.js',
    'flask': 'Flask',
    'django': 'Flask',
    'sql': 'SQL',
    'mysql': 'SQL',
    'postgresql': 'PostgreSQL',
    'postgres': 'PostgreSQL',
    'sqlite': 'SQL',
    'mongodb': 'SQL',
    'docker': 'Docker',
    'kubernetes': 'Kubernetes',
    'k8s': 'Kubernetes',
    'aws': 'AWS',
    'amazon web services': 'AWS',
    'gcp': 'AWS',
    'google cloud': 'AWS',
    'azure': 'AWS',
    'graphql': 'GraphQL',
    'rest api': 'GraphQL',
    'restful': 'GraphQL',
    'redis': 'Redis',
    'git': 'Git',
    'github': 'Git',
    'gitlab': 'Git',
    'pytorch': 'PyTorch',
    'tensorflow': 'TensorFlow',
    'machine learning': 'Machine Learning',
    'deep learning': 'Machine Learning',
    'ml': 'Machine Learning',
    'ai': 'Machine Learning',
    'artificial intelligence': 'Machine Learning',
    'system design': 'System Design',
    'data structures': 'Data Structures & Algorithms',
    'algorithms': 'Data Structures & Algorithms',
    'dsa': 'Data Structures & Algorithms',
    'css': 'UI/UX Design',
    'html': 'UI/UX Design',
    'ui': 'UI/UX Design',
    'ux': 'UI/UX Design',
    'figma': 'UI/UX Design',
    'terraform': 'Docker',
    'ci/cd': 'Docker',
    'jenkins': 'Docker',
    'linux': 'Git',
    'bash': 'Git',
    'shell': 'Git',
    'c++': 'Python',
    'c#': 'Python',
    'ruby': 'Python',
    'php': 'Python',
    'go': 'Python',
    'golang': 'Python',
    'rust': 'Python',
    'swift': 'Python',
    'kotlin': 'Python',
    'scala': 'Python',
    'r': 'Python',
    'matlab': 'Python',
    'excel': 'SQL',
    'tableau': 'SQL',
    'power bi': 'SQL',
    'jira': 'Git',
    'agile': 'Git',
    'scrum': 'Git',
    'microservices': 'System Design',
    'api': 'GraphQL',
    'testing': 'Git',
    'unit testing': 'Git',
    'selenium': 'Python',
    'pandas': 'Python',
    'numpy': 'Python',
    'scikit-learn': 'Machine Learning',
    'opencv': 'Machine Learning',
    'nlp': 'Machine Learning',
    'natural language processing': 'Machine Learning',
    'cassandra': 'SQL',
    'elasticsearch': 'Redis',
    'kafka': 'Redis',
    'rabbitmq': 'Redis',
    'nginx': 'Docker',
    'apache': 'Docker',
}


def extract_text_from_pdf(file_path):
    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(file_path)
        text = ''
        for page in reader.pages:
            text += page.extract_text() or ''
        return text
    except Exception:
        return ''


def extract_text_from_docx(file_path):
    try:
        from docx import Document
        doc = Document(file_path)
        text = '\n'.join([para.text for para in doc.paragraphs])
        return text
    except Exception:
        return ''


def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
        return extract_text_from_pdf(file_path)
    elif ext in ('.docx', '.doc'):
        return extract_text_from_docx(file_path)
    elif ext == '.txt':
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    return ''


def extract_skills_from_resume(file_path):
    text = extract_text(file_path)
    if not text:
        return [], text

    text_lower = text.lower()
    found = {}

    for keyword, skill_name in KNOWN_SKILLS.items():
        pattern = r'\b' + re.escape(keyword) + r'\b'
        if re.search(pattern, text_lower):
            if skill_name not in found:
                found[skill_name] = keyword

    return list(found.keys()), text


def match_resume_skills_to_db(detected_skills, all_db_skills):
    matched = []
    for db_skill in all_db_skills:
        if db_skill.name in detected_skills:
            matched.append(db_skill)
    return matched
