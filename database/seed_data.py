from database.firestore_db import get_db
from werkzeug.security import generate_password_hash
from datetime import datetime


def seed_database():
    db = get_db()
    if not db:
        print("[Seed] Firestore not available.")
        return

    existing = list(db.collection('users').limit(1).stream())
    if existing:
        print("[Seed] Database already contains data. Skipping.")
        return

    # 1. Companies
    companies_data = [
        {"name": "Google", "industry": "Artificial Intelligence & Cloud", "location": "Mountain View, CA / Remote", "logo_url": "https://img.icons8.com/color/144/google-logo.png", "description": "Google's mission is to organize the world's information and make it universally accessible and useful.", "website": "https://careers.google.com"},
        {"name": "Microsoft", "industry": "Enterprise Software & AI", "location": "Redmond, WA / Hybrid", "logo_url": "https://img.icons8.com/color/144/microsoft.png", "description": "Empowering every person and every organization on the planet to achieve more.", "website": "https://careers.microsoft.com"},
        {"name": "Meta", "industry": "Social Infrastructure & Metaverse", "location": "Menlo Park, CA / Remote", "logo_url": "https://img.icons8.com/color/144/meta.png", "description": "Meta builds technologies that help people connect and grow businesses.", "website": "https://metacareers.com"},
        {"name": "Amazon", "industry": "Cloud & E-Commerce", "location": "Seattle, WA / Hybrid", "logo_url": "https://img.icons8.com/color/144/amazon.png", "description": "Pioneering cloud architecture via AWS and machine learning infrastructure.", "website": "https://amazon.jobs"},
        {"name": "Stripe", "industry": "Financial Infrastructure", "location": "San Francisco, CA / Remote", "logo_url": "https://img.icons8.com/color/144/stripe.png", "description": "Stripe is a financial infrastructure platform for businesses.", "website": "https://stripe.com/jobs"},
    ]

    company_ids = {}
    for i, c in enumerate(companies_data, 1):
        cid = str(i)
        company_ids[c["name"]] = cid
        db.collection('companies').document(cid).set({"id": cid, **c})

    # 2. Skills
    skills_list = [
        ("Python", "Programming Languages"), ("Flask", "Web Development"), ("React", "Frontend"),
        ("JavaScript", "Programming Languages"), ("TypeScript", "Programming Languages"), ("SQL", "Database"),
        ("PostgreSQL", "Database"), ("Docker", "DevOps & Cloud"), ("Kubernetes", "DevOps & Cloud"),
        ("PyTorch", "Machine Learning / AI"), ("TensorFlow", "Machine Learning / AI"),
        ("Machine Learning", "Machine Learning / AI"), ("AWS", "DevOps & Cloud"),
        ("System Design", "Core Computer Science"), ("Data Structures & Algorithms", "Core Computer Science"),
        ("Node.js", "Backend"), ("GraphQL", "API Design"), ("Redis", "Database & Caching"),
        ("Git", "Tools"), ("UI/UX Design", "Design"),
    ]

    skill_ids = {}
    for i, (name, cat) in enumerate(skills_list, 1):
        sid = str(i)
        skill_ids[name] = sid
        db.collection('skills').document(sid).set({"id": sid, "name": name, "category": cat})

    # 3. Users
    cand_hash = generate_password_hash("password123", method='pbkdf2:sha256')
    db.collection('users').document("1").set({
        "id": "1", "name": "Alex Johnson", "email": "candidate@skillsbridge.com",
        "password_hash": cand_hash, "role": "candidate",
        "headline": "Full Stack Software Engineer & ML Enthusiast",
        "bio": "Passionate developer eager to upskill.", "company_id": None,
        "created_at": datetime.utcnow().isoformat(),
    })

    emp1_hash = generate_password_hash("password123", method='pbkdf2:sha256')
    db.collection('users').document("2").set({
        "id": "2", "name": "Sarah Jenkins", "email": "recruiter@google.com",
        "password_hash": emp1_hash, "role": "employer",
        "headline": "Senior Tech Recruiter at Google AI & Cloud",
        "bio": "Hiring top-tier engineering talent.", "company_id": company_ids["Google"],
        "created_at": datetime.utcnow().isoformat(),
    })

    emp2_hash = generate_password_hash("password123", method='pbkdf2:sha256')
    db.collection('users').document("3").set({
        "id": "3", "name": "David Chen", "email": "recruiter@microsoft.com",
        "password_hash": emp2_hash, "role": "employer",
        "headline": "Engineering Hiring Lead at Microsoft Azure",
        "bio": "Building the future of distributed systems.", "company_id": company_ids["Microsoft"],
        "created_at": datetime.utcnow().isoformat(),
    })

    # 4. Candidate skills for Alex
    alex_skills = [("Python", "Advanced"), ("JavaScript", "Intermediate"), ("SQL", "Intermediate"), ("Flask", "Intermediate"), ("Git", "Advanced")]
    for i, (sk_name, prof) in enumerate(alex_skills, 1):
        db.collection('candidate_skills').document(str(i)).set({
            "id": str(i), "user_id": "1", "skill_id": skill_ids[sk_name], "proficiency": prof,
        })

    # 5. Job postings
    jobs_data = [
        {"cid": company_ids["Google"], "title": "Software Engineer II - Cloud Backend", "domain": "Backend Engineering", "exp": "2-4 yrs", "loc": "Mountain View, CA / Hybrid", "sal": "$140,000 - $185,000 / yr", "desc": "Design scalable distributed backend systems processing millions of operations per second.", "skills": [("Python", "Advanced"), ("SQL", "Intermediate"), ("Docker", "Intermediate"), ("System Design", "Advanced"), ("Redis", "Intermediate")]},
        {"cid": company_ids["Google"], "title": "Machine Learning Engineer - AI Research", "domain": "AI / Machine Learning", "exp": "3-5 yrs", "loc": "San Francisco, CA / Remote", "sal": "$160,000 - $210,000 / yr", "desc": "Build state-of-the-art neural architecture models and optimize LLM inference pipelines.", "skills": [("Python", "Expert"), ("PyTorch", "Advanced"), ("TensorFlow", "Advanced"), ("Machine Learning", "Advanced"), ("Data Structures & Algorithms", "Advanced")]},
        {"cid": company_ids["Microsoft"], "title": "Full Stack Engineer - Azure Cloud Studio", "domain": "Software Development", "exp": "1-3 yrs", "loc": "Redmond, WA / Hybrid", "sal": "$125,000 - $165,000 / yr", "desc": "Building next-generation cloud developer tooling with React, TypeScript, and Node.js.", "skills": [("React", "Advanced"), ("TypeScript", "Intermediate"), ("Node.js", "Intermediate"), ("GraphQL", "Intermediate"), ("AWS", "Intermediate")]},
        {"cid": company_ids["Meta"], "title": "Senior Frontend Engineer - React Infrastructure", "domain": "Frontend Engineering", "exp": "4+ yrs", "loc": "Menlo Park, CA / Remote", "sal": "$175,000 - $230,000 / yr", "desc": "Architect core React web framework libraries powering Instagram and Facebook.", "skills": [("React", "Expert"), ("JavaScript", "Expert"), ("TypeScript", "Advanced"), ("UI/UX Design", "Intermediate")]},
        {"cid": company_ids["Amazon"], "title": "DevOps / Infrastructure Engineer - AWS Platform", "domain": "DevOps & Cloud", "exp": "2-5 yrs", "loc": "Seattle, WA / Remote", "sal": "$135,000 - $175,000 / yr", "desc": "Manage containerization pipelines, Kubernetes clusters, and Terraform infrastructure.", "skills": [("AWS", "Advanced"), ("Docker", "Advanced"), ("Kubernetes", "Advanced"), ("Python", "Intermediate")]},
        {"cid": company_ids["Stripe"], "title": "Backend Systems Engineer - Financial Core", "domain": "Backend Engineering", "exp": "2-4 yrs", "loc": "San Francisco, CA / Remote", "sal": "$150,000 - $190,000 / yr", "desc": "Develop mission-critical payment processing pipelines with sub-10ms response times.", "skills": [("Python", "Advanced"), ("PostgreSQL", "Advanced"), ("System Design", "Advanced"), ("Redis", "Intermediate")]},
    ]

    from datetime import datetime as _dt
    for i, jd in enumerate(jobs_data, 1):
        jid = str(i)
        db.collection('job_postings').document(jid).set({
            "id": jid, "company_id": jd["cid"], "title": jd["title"], "domain": jd["domain"],
            "experience_required": jd["exp"], "location": jd["loc"], "salary_range": jd["sal"],
            "description": jd["desc"], "created_at": datetime.utcnow().isoformat(),
        })
        for j, (sk_name, lvl) in enumerate(jd["skills"], 1):
            rid = f"{i}_{j}"
            db.collection('job_skill_requirements').document(rid).set({
                "id": rid, "job_id": jid, "skill_id": skill_ids[sk_name], "required_level": lvl,
            })

    # 6. Courses
    courses_data = [
        {"skill": "Docker", "title": "Docker for Absolute Beginners & DevOps Integration", "provider": "YouTube Tech", "type": "youtube", "url": "https://www.youtube.com/watch?v=fqMOX6JJhGo", "duration": "3 Hours", "diff": "Beginner"},
        {"skill": "Docker", "title": "Complete Docker Masterclass: From Zero to Container Hero", "provider": "Coursera", "type": "platform", "url": "https://www.coursera.org/learn/docker-containers", "duration": "4 Weeks", "diff": "Intermediate"},
        {"skill": "Docker", "title": "Google Cloud Containerization Specialist", "provider": "Google", "type": "company", "url": "https://cloud.google.com/training/containers", "duration": "2 Weeks", "diff": "Advanced"},
        {"skill": "System Design", "title": "System Design Primer & Scalable Architecture Blueprint", "provider": "GitHub Community", "type": "platform", "url": "https://github.com/donnemartin/system-design-primer", "duration": "Self-Paced", "diff": "Advanced"},
        {"skill": "System Design", "title": "High-Volume Backend Architecture Crash Course", "provider": "YouTube", "type": "youtube", "url": "https://www.youtube.com/watch?v=xpDnVSmNfx0", "duration": "4 Hours", "diff": "Intermediate"},
        {"skill": "PyTorch", "title": "PyTorch for Deep Learning & Neural Networks Bootcamp", "provider": "freeCodeCamp", "type": "youtube", "url": "https://www.youtube.com/watch?v=V_xro1bcAuA", "duration": "10 Hours", "diff": "Intermediate"},
        {"skill": "PyTorch", "title": "Google AI Deep Learning Specialization", "provider": "Google", "type": "company", "url": "https://ai.google/education/", "duration": "6 Weeks", "diff": "Advanced"},
        {"skill": "Kubernetes", "title": "Kubernetes Architecture & Production Cluster Administration", "provider": "edX", "type": "platform", "url": "https://www.edx.org/course/introduction-to-kubernetes", "duration": "5 Weeks", "diff": "Intermediate"},
        {"skill": "Kubernetes", "title": "K8s Hands-on Deployment Tutorial", "provider": "YouTube", "type": "youtube", "url": "https://www.youtube.com/watch?v=X48VuDVv0do", "duration": "4 Hours", "diff": "Beginner"},
        {"skill": "React", "title": "React 18 & Redux Toolkit Full Course", "provider": "YouTube", "type": "youtube", "url": "https://www.youtube.com/watch?v=bMknfKXIFA8", "duration": "12 Hours", "diff": "Beginner"},
        {"skill": "React", "title": "Meta Front-End Developer Professional Certificate", "provider": "Meta", "type": "company", "url": "https://www.coursera.org/professional-certificates/meta-front-end-developer", "duration": "8 Weeks", "diff": "Intermediate"},
        {"skill": "Redis", "title": "Redis In-Memory Caching & Pub-Sub Deep Dive", "provider": "Redis University", "type": "platform", "url": "https://university.redis.com/", "duration": "2 Weeks", "diff": "Intermediate"},
        {"skill": "PostgreSQL", "title": "Advanced SQL & Relational Database Design", "provider": "Udemy", "type": "platform", "url": "https://www.udemy.com/course/sql-and-postgresql/", "duration": "3 Weeks", "diff": "Intermediate"},
    ]

    for i, cd in enumerate(courses_data, 1):
        db.collection('courses').document(str(i)).set({
            "id": str(i), "skill_id": skill_ids[cd["skill"]], "title": cd["title"],
            "provider": cd["provider"], "source_type": cd["type"], "url": cd["url"],
            "duration": cd["duration"], "difficulty": cd["diff"], "employer_id": None,
        })

    # 7. Interview resources
    interview_res = [
        {"cid": company_ids["Google"], "title": "Google Technical Interview Cheat Sheet (Coding + DSA)", "url": "https://careers.google.com/how-we-hire/interview/", "type": "Coding Prep", "desc": "Official Google guide covering algorithmic problem solving and live coding."},
        {"cid": company_ids["Google"], "title": "Google System Design & Distributed Systems Round", "url": "https://github.com/checkcheckzz/system-design-interview", "type": "System Design", "desc": "Real questions asked during Google Cloud and Search system design rounds."},
        {"cid": company_ids["Google"], "title": "Google Leadership Principles & Behavioral Questions", "url": "https://www.google.com/about/careers/applications/interview-tips/", "type": "HR Prep", "desc": "Googleliness and leadership question framework using STAR technique."},
        {"cid": company_ids["Microsoft"], "title": "Microsoft Technical Phone Screen & Onsite Guide", "url": "https://careers.microsoft.com/v2/global/en/hiring-process.html", "type": "Question Bank", "desc": "Detailed overview of Microsoft technical rounds and live whiteboarding."},
        {"cid": company_ids["Meta"], "title": "Meta Product Architecture & React Deep Dive", "url": "https://metacareers.com/prep/", "type": "Coding Prep", "desc": "Speed coding tips, binary tree traversals, and frontend system architecture."},
        {"cid": company_ids["Stripe"], "title": "Stripe Integration & Bug Bash Practical Round", "url": "https://stripe.com/jobs/tech-interview-prep", "type": "Coding Prep", "desc": "Hands-on API debugging and refactoring round expectations at Stripe."},
    ]

    for i, ir in enumerate(interview_res, 1):
        db.collection('interview_resources').document(str(i)).set({
            "id": str(i), "company_id": ir["cid"], "job_id": None, "title": ir["title"],
            "url": ir["url"], "resource_type": ir["type"], "description": ir["desc"],
        })

    print("[Seed] Firestore database successfully seeded!")
