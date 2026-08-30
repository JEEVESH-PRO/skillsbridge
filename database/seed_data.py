from database.firestore_db import get_db

def seed_database():
    db = get_db()
    existing = list(db.collection('users').limit(1).stream())
    if existing:
        print("[Seed] Firestore database already contains data. Skipping.")
        return

    print("[Seed] Seeding real-time companies, skills, jobs, and courses into Firestore...")

    # 1. Companies Data categorized by Product-Based, Service-Based, AI/DeepTech, Fintech, Semiconductors
    companies_data = [
        # Product-Based IT
        {
            "id": "1", "name": "Google", "industry": "Product-Based IT", "location": "Mountain View, CA / Remote",
            "logo_url": "https://img.icons8.com/color/144/google-logo.png",
            "description": "Global technology giant specializing in search, cloud infrastructure, AI models, and consumer products.",
            "website": "https://careers.google.com"
        },
        {
            "id": "2", "name": "Microsoft", "industry": "Product-Based IT", "location": "Redmond, WA / Hybrid",
            "logo_url": "https://img.icons8.com/color/144/microsoft.png",
            "description": "Empowering every person and organization through Azure cloud, OpenAI partnership, Windows, and enterprise tools.",
            "website": "https://careers.microsoft.com"
        },
        {
            "id": "3", "name": "Meta", "industry": "Product-Based IT", "location": "Menlo Park, CA / Remote",
            "logo_url": "https://img.icons8.com/color/144/meta.png",
            "description": "Pioneering AI open source (Llama), social networks (Instagram, WhatsApp, Threads), and metaverse hardware.",
            "website": "https://metacareers.com"
        },
        {
            "id": "4", "name": "Apple", "industry": "Product-Based IT", "location": "Cupertino, CA / Hybrid",
            "logo_url": "https://img.icons8.com/color/144/apple-logo.png",
            "description": "World-leading hardware and software engineering powering iOS, macOS, Apple Silicon, and AI ecosystem.",
            "website": "https://jobs.apple.com"
        },
        {
            "id": "5", "name": "Amazon", "industry": "Product-Based IT", "location": "Seattle, WA / Hybrid",
            "logo_url": "https://img.icons8.com/color/144/amazon.png",
            "description": "Global e-commerce leader and cloud innovator operating AWS, Bedrock AI, and automated logistics.",
            "website": "https://amazon.jobs"
        },
        {
            "id": "6", "name": "OpenAI", "industry": "AI & DeepTech", "location": "San Francisco, CA / Hybrid",
            "logo_url": "https://img.icons8.com/ios-filled/150/ffffff/chatgpt.png",
            "description": "AI research and deployment company behind ChatGPT, GPT-4, and frontier generative AI models.",
            "website": "https://openai.com/careers"
        },
        
        # Service-Based IT & Consulting
        {
            "id": "7", "name": "TCS (Tata Consultancy Services)", "industry": "Service-Based IT", "location": "Mumbai, India / Global",
            "logo_url": "https://img.icons8.com/color/144/briefcase.png",
            "description": "Leading global IT services, consulting, and business solutions enterprise operating in 55+ countries.",
            "website": "https://www.tcs.com/careers"
        },
        {
            "id": "8", "name": "Infosys", "industry": "Service-Based IT", "location": "Bengaluru, India / Global",
            "logo_url": "https://img.icons8.com/color/144/company.png",
            "description": "Global leader in next-generation digital services, cloud transformation, and enterprise consulting.",
            "website": "https://www.infosys.com/careers"
        },
        {
            "id": "9", "name": "Accenture", "industry": "Service-Based IT", "location": "Dublin, Ireland / Global",
            "logo_url": "https://img.icons8.com/color/144/accenture.png",
            "description": "Leading global professional services company specializing in digital, cloud, cybersecurity, and AI strategy.",
            "website": "https://www.accenture.com/careers"
        },
        {
            "id": "10", "name": "Cognizant", "industry": "Service-Based IT", "location": "Teaneck, NJ / Global",
            "logo_url": "https://img.icons8.com/color/144/organization.png",
            "description": "Engineers modern business models to modernize technology, reimagine processes, and transform customer experiences.",
            "website": "https://www.cognizant.com/careers"
        },

        # Fintech
        {
            "id": "11", "name": "Stripe", "industry": "Fintech", "location": "San Francisco, CA / Remote",
            "logo_url": "https://img.icons8.com/color/144/stripe.png",
            "description": "Financial infrastructure platform for businesses, powering payments, subscriptions, and banking services worldwide.",
            "website": "https://stripe.com/jobs"
        },

        # Semiconductors & DeepTech
        {
            "id": "12", "name": "NVIDIA", "industry": "Hardware & Semiconductors", "location": "Santa Clara, CA / Hybrid",
            "logo_url": "https://img.icons8.com/color/144/nvidia.png",
            "description": "Inventor of the GPU, powering modern generative AI, supercomputing, autonomous machines, and omniverse.",
            "website": "https://www.nvidia.com/careers"
        }
    ]

    for c in companies_data:
        db.collection('companies').document(c['id']).set(c)

    # 2. Global Technical Skills Dictionary
    skills_data = [
        ("1", "Python", "Programming Languages"),
        ("2", "JavaScript", "Programming Languages"),
        ("3", "TypeScript", "Programming Languages"),
        ("4", "Java", "Programming Languages"),
        ("5", "C++", "Programming Languages"),
        ("6", "Go", "Programming Languages"),
        ("7", "Rust", "Programming Languages"),
        ("8", "SQL", "Database"),
        ("9", "Flask", "Web Development"),
        ("10", "React", "Frontend"),
        ("11", "Next.js", "Frontend"),
        ("12", "Node.js", "Backend"),
        ("13", "Docker", "DevOps & Cloud"),
        ("14", "Kubernetes", "DevOps & Cloud"),
        ("15", "PyTorch", "Machine Learning / AI"),
        ("16", "TensorFlow", "Machine Learning / AI"),
        ("17", "Machine Learning", "Machine Learning / AI"),
        ("18", "AWS", "DevOps & Cloud"),
        ("19", "PostgreSQL", "Database"),
        ("20", "Redis", "Database & Caching"),
        ("21", "System Design", "Core Computer Science"),
        ("22", "Data Structures & Algorithms", "Core Computer Science"),
        ("23", "GraphQL", "API Design"),
        ("24", "Git", "Tools"),
        ("25", "UI/UX Design", "Design")
    ]

    for sk_id, name, cat in skills_data:
        db.collection('skills').document(sk_id).set({"id": sk_id, "name": name, "category": cat})

    # 3. Seed Candidate & Employer Users
    from werkzeug.security import generate_password_hash
    cand_user = {
        "id": "1", "name": "Alex Johnson", "email": "candidate@skillsbridge.com",
        "password_hash": generate_password_hash("password123", method="pbkdf2:sha256"),
        "role": "candidate", "headline": "Full Stack Developer & AI Enthusiast",
        "bio": "Passionate software engineer building web apps and deep learning models.",
        "company_id": None, "created_at": "2026-08-27T00:00:00"
    }
    db.collection('users').document("1").set(cand_user)

    google_emp = {
        "id": "2", "name": "Sarah Jenkins", "email": "recruiter@google.com",
        "password_hash": generate_password_hash("password123", method="pbkdf2:sha256"),
        "role": "employer", "headline": "Senior Engineering Recruiter at Google",
        "bio": "Hiring top backend, cloud, and AI engineering talent for Google Search and AI.",
        "company_id": "1", "created_at": "2026-08-27T00:00:00"
    }
    db.collection('users').document("2").set(google_emp)

    msft_emp = {
        "id": "3", "name": "David Chen", "email": "recruiter@microsoft.com",
        "password_hash": generate_password_hash("password123", method="pbkdf2:sha256"),
        "role": "employer", "headline": "Hiring Manager at Microsoft Azure",
        "bio": "Building scalable cloud computing platforms and developer tools.",
        "company_id": "2", "created_at": "2026-08-27T00:00:00"
    }
    db.collection('users').document("3").set(msft_emp)

    # Candidate Initial Skills
    cand_skills = [
        ("1_1", "1", "1", "Advanced"),    # Python
        ("1_2", "1", "2", "Intermediate"),# JS
        ("1_8", "1", "8", "Intermediate"),# SQL
        ("1_9", "1", "9", "Intermediate"),# Flask
        ("1_24", "1", "24", "Advanced")   # Git
    ]
    for cs_id, uid, sid, prof in cand_skills:
        db.collection('candidate_skills').document(cs_id).set({"id": cs_id, "user_id": uid, "skill_id": sid, "proficiency": prof})

    # 4. Job Postings across categories
    jobs_data = [
        {
            "id": "1", "company_id": "1", "title": "Software Engineer II - Cloud Backend",
            "domain": "Product-Based IT", "experience_required": "2-4 yrs", "location": "Mountain View, CA / Remote",
            "salary_range": "$140,000 - $185,000 / yr",
            "description": "Architect scalable distributed microservices processing millions of RPCs per second for Google Cloud Platform."
        },
        {
            "id": "2", "company_id": "6", "title": "Research Engineer - LLM & Reasoning",
            "domain": "AI & DeepTech", "experience_required": "3-5 yrs", "location": "San Francisco, CA / Hybrid",
            "salary_range": "$220,000 - $350,000 / yr",
            "description": "Train frontier generative models, optimize distributed GPU cluster inference, and design agentic architectures."
        },
        {
            "id": "3", "company_id": "2", "title": "Full Stack Cloud Developer - Azure Studio",
            "domain": "Product-Based IT", "experience_required": "1-3 yrs", "location": "Redmond, WA / Hybrid",
            "salary_range": "$125,000 - $165,000 / yr",
            "description": "Building developer infrastructure tools powered by React, TypeScript, Node.js, and Azure microservices."
        },
        {
            "id": "4", "company_id": "7", "title": "Senior Technical Lead - Enterprise Cloud",
            "domain": "Service-Based IT", "experience_required": "5+ yrs", "location": "Bengaluru, India / Remote",
            "salary_range": "₹24,00,000 - ₹35,00,000 / yr",
            "description": "Leading global client migration to cloud-native microservices architecture, CI/CD automation, and DevOps."
        },
        {
            "id": "5", "company_id": "11", "title": "Backend Systems Engineer - Financial Core",
            "domain": "Fintech", "experience_required": "2-4 yrs", "location": "San Francisco, CA / Remote",
            "salary_range": "$150,000 - $190,000 / yr",
            "description": "Develop mission-critical payment processing pipelines with sub-10ms response times and fault tolerance."
        },
        {
            "id": "6", "company_id": "12", "title": "CUDA Systems & Parallel Compiler Engineer",
            "domain": "Hardware & Semiconductors", "experience_required": "3+ yrs", "location": "Santa Clara, CA / Hybrid",
            "salary_range": "$180,000 - $240,000 / yr",
            "description": "Optimize low-level GPU acceleration, CUDA kernels, and deep learning compiler backends for AI hardware."
        }
    ]

    for j in jobs_data:
        db.collection('job_postings').document(j['id']).set(j)

    # Job Skill Requirements
    job_reqs = [
        # Job 1 (Google Cloud)
        ("1_1", "1", "1", "Advanced"),     # Python
        ("1_8", "1", "8", "Intermediate"), # SQL
        ("1_13", "1", "13", "Intermediate"),# Docker
        ("1_21", "1", "21", "Advanced"),   # System Design
        ("1_20", "1", "20", "Intermediate"),# Redis

        # Job 2 (OpenAI)
        ("2_1", "2", "1", "Expert"),       # Python
        ("2_15", "2", "15", "Advanced"),   # PyTorch
        ("2_16", "2", "16", "Advanced"),   # TensorFlow
        ("2_17", "2", "17", "Advanced"),   # Machine Learning
        ("2_22", "2", "22", "Advanced"),   # DSA

        # Job 3 (Microsoft)
        ("3_10", "3", "10", "Advanced"),   # React
        ("3_3", "3", "3", "Intermediate"), # TypeScript
        ("3_12", "3", "12", "Intermediate"),# Node.js
        ("3_18", "3", "18", "Intermediate"),# AWS

        # Job 4 (TCS)
        ("4_18", "4", "18", "Advanced"),   # AWS
        ("4_13", "4", "13", "Advanced"),   # Docker
        ("4_14", "4", "14", "Advanced"),   # Kubernetes
        ("4_1", "4", "1", "Intermediate"), # Python

        # Job 5 (Stripe)
        ("5_1", "5", "1", "Advanced"),     # Python
        ("5_19", "5", "19", "Advanced"),   # PostgreSQL
        ("5_21", "5", "21", "Advanced"),   # System Design
        ("5_20", "5", "20", "Intermediate"),# Redis

        # Job 6 (NVIDIA)
        ("5_5", "6", "5", "Expert"),       # C++
        ("5_1", "6", "1", "Advanced"),     # Python
        ("5_22", "6", "22", "Advanced")    # DSA
    ]

    for req_id, jid, sid, req_lvl in job_reqs:
        db.collection('job_skill_requirements').document(req_id).set({"id": req_id, "job_id": jid, "skill_id": sid, "required_level": req_lvl})

    # 5. Courses Data
    courses_data = [
        {"id": "1", "skill_id": "13", "title": "Docker Containerization & Kubernetes Mastery", "provider": "Coursera", "source_type": "platform", "url": "https://www.coursera.org/learn/docker-containers", "duration": "4 Weeks", "difficulty": "Intermediate"},
        {"id": "2", "skill_id": "13", "title": "Docker for Absolute Beginners", "provider": "YouTube", "source_type": "youtube", "url": "https://www.youtube.com/watch?v=fqMOX6JJhGo", "duration": "3 Hours", "difficulty": "Beginner"},
        {"id": "3", "skill_id": "21", "title": "System Design Primer & High Scale Systems", "provider": "GitHub Community", "source_type": "platform", "url": "https://github.com/donnemartin/system-design-primer", "duration": "Self-Paced", "difficulty": "Advanced"},
        {"id": "4", "skill_id": "15", "title": "PyTorch for Deep Learning & Neural Networks", "provider": "freeCodeCamp", "source_type": "youtube", "url": "https://www.youtube.com/watch?v=V_xro1bcAuA", "duration": "10 Hours", "difficulty": "Intermediate"},
        {"id": "5", "skill_id": "10", "title": "React 18 & Next.js Full Stack Development", "provider": "YouTube", "source_type": "youtube", "url": "https://www.youtube.com/watch?v=bMknfKXIFA8", "duration": "12 Hours", "difficulty": "Intermediate"},
        {"id": "6", "skill_id": "14", "title": "Kubernetes Cluster Administration", "provider": "edX", "source_type": "platform", "url": "https://www.edx.org/course/introduction-to-kubernetes", "duration": "5 Weeks", "difficulty": "Intermediate"}
    ]

    for c in courses_data:
        db.collection('courses').document(c['id']).set(c)

    # 6. Interview Resources
    interview_data = [
        {
            "id": "1", "company_id": "1", "title": "Google Technical Interview Cheat Sheet (Coding + DSA)",
            "url": "https://careers.google.com/how-we-hire/interview/", "resource_type": "Coding Prep",
            "description": "Official Google guide covering algorithmic problem solving, time complexity analysis, and live coding expectations."
        },
        {
            "id": "2", "company_id": "1", "title": "Google System Design & Distributed Systems Blueprint",
            "url": "https://github.com/checkcheckzz/system-design-interview", "resource_type": "System Design",
            "description": "Real questions asked during Google Cloud and Search system design rounds."
        },
        {
            "id": "3", "company_id": "6", "title": "OpenAI Machine Learning & PyTorch Deep Dive",
            "url": "https://openai.com/research/", "resource_type": "AI Prep",
            "description": "Neural architecture, LLM fine-tuning, and CUDA memory optimization guides."
        },
        {
            "id": "4", "company_id": "2", "title": "Microsoft Technical Phone Screen & Onsite Guide",
            "url": "https://careers.microsoft.com/v2/global/en/hiring-process.html", "resource_type": "Question Bank",
            "description": "Detailed overview of Microsoft technical rounds and OOP design challenges."
        }
    ]

    for ir in interview_data:
        db.collection('interview_resources').document(ir['id']).set(ir)

    print("[Seed] Firestore database successfully seeded!")
