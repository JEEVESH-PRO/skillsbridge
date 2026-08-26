from models import db
from models.user import User
from models.company import Company
from models.skill import Skill, CandidateSkill
from models.job import JobPosting, JobSkillRequirement
from models.course import Course
from models.interview_resource import InterviewResource

def seed_database():
    print("Seeding database...")

    # Clear existing data if needed or skip if already seeded
    if User.query.first() is not None:
        print("Database already contains data. Skipping seed.")
        return

    # 1. Add Companies
    companies_data = [
        {
            "name": "Google",
            "industry": "Artificial Intelligence & Cloud",
            "location": "Mountain View, CA / Remote",
            "logo_url": "https://img.icons8.com/color/144/google-logo.png",
            "description": "Google's mission is to organize the world's information and make it universally accessible and useful. Build products that impact billions of users worldwide.",
            "website": "https://careers.google.com"
        },
        {
            "name": "Microsoft",
            "industry": "Enterprise Software & AI",
            "location": "Redmond, WA / Hybrid",
            "logo_url": "https://img.icons8.com/color/144/microsoft.png",
            "description": "Empowering every person and every organization on the planet to achieve more through cloud computing, AI, and developer platform innovations.",
            "website": "https://careers.microsoft.com"
        },
        {
            "name": "Meta",
            "industry": "Social Infrastructure & Metaverse",
            "location": "Menlo Park, CA / Remote",
            "logo_url": "https://img.icons8.com/color/144/meta.png",
            "description": "Meta builds technologies that help people connect, find communities, and grow businesses across Facebook, Instagram, WhatsApp, and AI infrastructure.",
            "website": "https://metacareers.com"
        },
        {
            "name": "Amazon",
            "industry": "Cloud & E-Commerce",
            "location": "Seattle, WA / Hybrid",
            "logo_url": "https://img.icons8.com/color/144/amazon.png",
            "description": "Pioneering cloud architecture via AWS, robotics, digital streaming, and machine learning infrastructure globally.",
            "website": "https://amazon.jobs"
        },
        {
            "name": "Stripe",
            "industry": "Financial Infrastructure",
            "location": "San Francisco, CA / Remote",
            "logo_url": "https://img.icons8.com/color/144/stripe.png",
            "description": "Stripe is a financial infrastructure platform for businesses. Millions of companies from ambitious startups to Fortune 500s use Stripe.",
            "website": "https://stripe.com/jobs"
        }
    ]

    company_objs = {}
    for c in companies_data:
        comp = Company(**c)
        db.session.add(comp)
        company_objs[c["name"]] = comp
    db.session.commit()

    # 2. Add Skills
    skills_list = [
        ("Python", "Programming Languages"),
        ("Flask", "Web Development"),
        ("React", "Frontend"),
        ("JavaScript", "Programming Languages"),
        ("TypeScript", "Programming Languages"),
        ("SQL", "Database"),
        ("PostgreSQL", "Database"),
        ("Docker", "DevOps & Cloud"),
        ("Kubernetes", "DevOps & Cloud"),
        ("PyTorch", "Machine Learning / AI"),
        ("TensorFlow", "Machine Learning / AI"),
        ("Machine Learning", "Machine Learning / AI"),
        ("AWS", "DevOps & Cloud"),
        ("System Design", "Core Computer Science"),
        ("Data Structures & Algorithms", "Core Computer Science"),
        ("Node.js", "Backend"),
        ("GraphQL", "API Design"),
        ("Redis", "Database & Caching"),
        ("Git", "Tools"),
        ("UI/UX Design", "Design")
    ]

    skill_objs = {}
    for name, category in skills_list:
        sk = Skill(name=name, category=category)
        db.session.add(sk)
        skill_objs[name] = sk
    db.session.commit()

    # 3. Add Users (Candidate & Employers)
    candidate_user = User(
        name="Alex Johnson",
        email="candidate@skillsbridge.com",
        role="candidate",
        headline="Full Stack Software Engineer & ML Enthusiast",
        bio="Passionate developer eager to upskill from entry level to senior engineering roles. Experienced in Python, JavaScript, and Web Technologies."
    )
    candidate_user.set_password("password123")
    db.session.add(candidate_user)

    google_employer = User(
        name="Sarah Jenkins",
        email="recruiter@google.com",
        role="employer",
        headline="Senior Tech Recruiter at Google AI & Cloud",
        bio="Hiring top-tier engineering talent for Google Search, Brain, and Cloud Platform.",
        company_id=company_objs["Google"].id
    )
    google_employer.set_password("password123")
    db.session.add(google_employer)

    msft_employer = User(
        name="David Chen",
        email="recruiter@microsoft.com",
        role="employer",
        headline="Engineering Hiring Lead at Microsoft Azure",
        bio="Building the future of distributed systems and cloud services.",
        company_id=company_objs["Microsoft"].id
    )
    msft_employer.set_password("password123")
    db.session.add(msft_employer)

    db.session.commit()

    # 4. Add Candidate Skills for Alex
    alex_skills = [
        ("Python", "Advanced"),
        ("JavaScript", "Intermediate"),
        ("SQL", "Intermediate"),
        ("Flask", "Intermediate"),
        ("Git", "Advanced")
    ]
    for sk_name, prof in alex_skills:
        cs = CandidateSkill(
            user_id=candidate_user.id,
            skill_id=skill_objs[sk_name].id,
            proficiency=prof
        )
        db.session.add(cs)
    db.session.commit()

    # 5. Add Job Postings
    jobs_data = [
        {
            "company_name": "Google",
            "title": "Software Engineer II - Cloud Backend",
            "domain": "Backend Engineering",
            "experience_required": "2-4 yrs",
            "location": "Mountain View, CA / Hybrid",
            "salary_range": "$140,000 - $185,000 / yr",
            "description": "As a Software Engineer at Google Cloud, you will design scalable distributed backend systems processing millions of operations per second. You will work closely with security, reliability, and modern database teams.",
            "skills": [("Python", "Advanced"), ("SQL", "Intermediate"), ("Docker", "Intermediate"), ("System Design", "Advanced"), ("Redis", "Intermediate")]
        },
        {
            "company_name": "Google",
            "title": "Machine Learning Engineer - AI Research",
            "domain": "AI / Machine Learning",
            "experience_required": "3-5 yrs",
            "location": "San Francisco, CA / Remote",
            "salary_range": "$160,000 - $210,000 / yr",
            "description": "Join Google AI to build state-of-the-art neural architecture models, optimize LLM inference pipelines, and implement deep learning algorithms in production.",
            "skills": [("Python", "Expert"), ("PyTorch", "Advanced"), ("TensorFlow", "Advanced"), ("Machine Learning", "Advanced"), ("Data Structures & Algorithms", "Advanced")]
        },
        {
            "company_name": "Microsoft",
            "title": "Full Stack Engineer - Azure Cloud Studio",
            "domain": "Software Development",
            "experience_required": "1-3 yrs",
            "location": "Redmond, WA / Hybrid",
            "salary_range": "$125,000 - $165,000 / yr",
            "description": "Building next-generation cloud developer tooling. Require proficiency in React, TypeScript, Node.js, and cloud backend microservices.",
            "skills": [("React", "Advanced"), ("TypeScript", "Intermediate"), ("Node.js", "Intermediate"), ("GraphQL", "Intermediate"), ("AWS", "Intermediate")]
        },
        {
            "company_name": "Meta",
            "title": "Senior Frontend Engineer - React Infrastructure",
            "domain": "Frontend Engineering",
            "experience_required": "4+ yrs",
            "location": "Menlo Park, CA / Remote",
            "salary_range": "$175,000 - $230,000 / yr",
            "description": "Architect core React web framework libraries powering Instagram and Facebook web clients worldwide. Deep knowledge of Web Vitals and DOM rendering performance required.",
            "skills": [("React", "Expert"), ("JavaScript", "Expert"), ("TypeScript", "Advanced"), ("UI/UX Design", "Intermediate")]
        },
        {
            "company_name": "Amazon",
            "title": "DevOps / Infrastructure Engineer - AWS Platform",
            "domain": "DevOps & Cloud",
            "experience_required": "2-5 yrs",
            "location": "Seattle, WA / Remote",
            "salary_range": "$135,000 - $175,000 / yr",
            "description": "Manage containerization pipelines, Kubernetes orchestration clusters, and automated Terraform infrastructure for AWS global customers.",
            "skills": [("AWS", "Advanced"), ("Docker", "Advanced"), ("Kubernetes", "Advanced"), ("Python", "Intermediate")]
        },
        {
            "company_name": "Stripe",
            "title": "Backend Systems Engineer - Financial Core",
            "domain": "Backend Engineering",
            "experience_required": "2-4 yrs",
            "location": "San Francisco, CA / Remote",
            "salary_range": "$150,000 - $190,000 / yr",
            "description": "Develop mission-critical payment processing pipelines with sub-10ms response times, transactional fault tolerance, and API elegance.",
            "skills": [("Python", "Advanced"), ("PostgreSQL", "Advanced"), ("System Design", "Advanced"), ("Redis", "Intermediate")]
        }
    ]

    job_objs = []
    for jdata in jobs_data:
        comp = company_objs[jdata["company_name"]]
        job = JobPosting(
            company_id=comp.id,
            title=jdata["title"],
            domain=jdata["domain"],
            experience_required=jdata["experience_required"],
            location=jdata["location"],
            salary_range=jdata["salary_range"],
            description=jdata["description"]
        )
        db.session.add(job)
        db.session.commit()
        job_objs.append(job)

        for sk_name, req_lvl in jdata["skills"]:
            if sk_name in skill_objs:
                req = JobSkillRequirement(
                    job_id=job.id,
                    skill_id=skill_objs[sk_name].id,
                    required_level=req_lvl
                )
                db.session.add(req)
        db.session.commit()

    # 6. Add Courses (Sourced learning for skills)
    courses_data = [
        # Docker
        {"skill": "Docker", "title": "Docker for Absolute Beginners & DevOps Integration", "provider": "YouTube Tech", "type": "youtube", "url": "https://www.youtube.com/watch?v=fqMOX6JJhGo", "duration": "3 Hours", "diff": "Beginner"},
        {"skill": "Docker", "title": "Complete Docker Masterclass: From Zero to Container Hero", "provider": "Coursera Platform", "type": "platform", "url": "https://www.coursera.org/learn/docker-containers", "duration": "4 Weeks", "diff": "Intermediate"},
        {"skill": "Docker", "title": "Google Cloud Containerization Specialist", "provider": "Google Offered", "type": "company", "url": "https://cloud.google.com/training/containers", "duration": "2 Weeks", "diff": "Advanced", "employer": google_employer.id},

        # System Design
        {"skill": "System Design", "title": "System Design Primer & Scalable Architecture Blueprint", "provider": "GitHub Community", "type": "platform", "url": "https://github.com/donnemartin/system-design-primer", "duration": "Self-Paced", "diff": "Advanced"},
        {"skill": "System Design", "title": "High-Volume Backend Architecture Crash Course", "provider": "YouTube", "type": "youtube", "url": "https://www.youtube.com/watch?v=xpDnVSmNfx0", "duration": "4 Hours", "diff": "Intermediate"},
        
        # PyTorch / ML
        {"skill": "PyTorch", "title": "PyTorch for Deep Learning & Neural Networks Bootcamp", "provider": "freeCodeCamp", "type": "youtube", "url": "https://www.youtube.com/watch?v=V_xro1bcAuA", "duration": "10 Hours", "diff": "Intermediate"},
        {"skill": "PyTorch", "title": "Google AI Deep Learning Specialization", "provider": "Google Offered", "type": "company", "url": "https://ai.google/education/", "duration": "6 Weeks", "diff": "Advanced", "employer": google_employer.id},

        # Kubernetes
        {"skill": "Kubernetes", "title": "Kubernetes Architecture & Production Cluster Administration", "provider": "edX", "type": "platform", "url": "https://www.edx.org/course/introduction-to-kubernetes", "duration": "5 Weeks", "diff": "Intermediate"},
        {"skill": "Kubernetes", "title": "K8s Hands-on Deployment Tutorial", "provider": "YouTube", "type": "youtube", "url": "https://www.youtube.com/watch?v=X48VuDVv0do", "duration": "4 Hours", "diff": "Beginner"},

        # React
        {"skill": "React", "title": "React 18 & Redux Toolkit Full Course", "provider": "YouTube", "type": "youtube", "url": "https://www.youtube.com/watch?v=bMknfKXIFA8", "duration": "12 Hours", "diff": "Beginner"},
        {"skill": "React", "title": "Meta Front-End Developer Professional Certificate", "provider": "Meta Offered", "type": "company", "url": "https://www.coursera.org/professional-certificates/meta-front-end-developer", "duration": "8 Weeks", "diff": "Intermediate"},

        # Redis
        {"skill": "Redis", "title": "Redis In-Memory Caching & Pub-Sub Deep Dive", "provider": "Redis University", "type": "platform", "url": "https://university.redis.com/", "duration": "2 Weeks", "diff": "Intermediate"},

        # PostgreSQL
        {"skill": "PostgreSQL", "title": "Advanced SQL & Relational Database Design", "provider": "Udemy", "type": "platform", "url": "https://www.udemy.com/course/sql-and-postgresql/", "duration": "3 Weeks", "diff": "Intermediate"}
    ]

    for cdata in courses_data:
        sk_name = cdata["skill"]
        if sk_name in skill_objs:
            crs = Course(
                skill_id=skill_objs[sk_name].id,
                title=cdata["title"],
                provider=cdata["provider"],
                source_type=cdata["type"],
                url=cdata["url"],
                duration=cdata["duration"],
                difficulty=cdata["diff"],
                employer_id=cdata.get("employer")
            )
            db.session.add(crs)
    db.session.commit()

    # 7. Add Interview Resources for Companies
    interview_res = [
        {
            "company_name": "Google",
            "title": "Google Technical Interview Cheat Sheet (Coding + DSA)",
            "url": "https://careers.google.com/how-we-hire/interview/",
            "type": "Coding Prep",
            "desc": "Official Google guide covering algorithmic problem solving, time/space complexity analysis, and live coding expectations."
        },
        {
            "company_name": "Google",
            "title": "Google System Design & Distributed Systems Round",
            "url": "https://github.com/checkcheckzz/system-design-interview",
            "type": "System Design",
            "desc": "Real questions asked during Google Cloud and Search system design rounds including caching, sharding, and consensus protocols."
        },
        {
            "company_name": "Google",
            "title": "Google Leadership Principles & Behavioral Questions",
            "url": "https://www.google.com/about/careers/applications/interview-tips/",
            "type": "HR Prep",
            "desc": "Googleliness and leadership question framework using STAR technique responses."
        },
        {
            "company_name": "Microsoft",
            "title": "Microsoft Technical Phone Screen & Onsite Guide",
            "url": "https://careers.microsoft.com/v2/global/en/hiring-process.html",
            "type": "Question Bank",
            "desc": "Detailed overview of Microsoft technical rounds, OOP design challenges, and live whiteboarding."
        },
        {
            "company_name": "Meta",
            "title": "Meta Product Architecture & React Deep Dive",
            "url": "https://metacareers.com/prep/",
            "type": "Coding Prep",
            "desc": "Speed coding tips, binary tree traversals, and frontend system architecture for Meta engineering candidates."
        },
        {
            "company_name": "Stripe",
            "title": "Stripe Integration & Bug Bash Practical Round",
            "url": "https://stripe.com/jobs/tech-interview-prep",
            "type": "Coding Prep",
            "desc": "Hands-on API debugging and refactoring round expectations at Stripe."
        }
    ]

    for ir in interview_res:
        comp = company_objs[ir["company_name"]]
        resource = InterviewResource(
            company_id=comp.id,
            title=ir["title"],
            url=ir["url"],
            resource_type=ir["type"],
            description=ir["desc"]
        )
        db.session.add(resource)
    db.session.commit()

    print("Database successfully seeded!")
