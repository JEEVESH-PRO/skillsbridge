-- Schema DDL for SkillsBridge

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'candidate', -- candidate / employer
    headline VARCHAR(200),
    bio TEXT,
    company_id INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(id)
);

CREATE TABLE IF NOT EXISTS companies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(120) UNIQUE NOT NULL,
    industry VARCHAR(100) NOT NULL,
    location VARCHAR(120),
    logo_url VARCHAR(256),
    description TEXT,
    website VARCHAR(256)
);

CREATE TABLE IF NOT EXISTS skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) UNIQUE NOT NULL,
    category VARCHAR(80) NOT NULL DEFAULT 'General'
);

CREATE TABLE IF NOT EXISTS candidate_skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    skill_id INTEGER NOT NULL,
    proficiency VARCHAR(50) NOT NULL DEFAULT 'Intermediate', -- Beginner, Intermediate, Advanced, Expert
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES skills(id) ON DELETE CASCADE,
    UNIQUE(user_id, skill_id)
);

CREATE TABLE IF NOT EXISTS job_postings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    title VARCHAR(150) NOT NULL,
    domain VARCHAR(80) NOT NULL, -- Software, AI/ML, DevOps, Data Science, Frontend, Backend, UI/UX
    experience_required VARCHAR(50) NOT NULL, -- 0-2 yrs, 2-5 yrs, 5+ yrs
    location VARCHAR(100) DEFAULT 'Remote',
    salary_range VARCHAR(80),
    description TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS job_skill_requirements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER NOT NULL,
    skill_id INTEGER NOT NULL,
    required_level VARCHAR(50) DEFAULT 'Intermediate',
    FOREIGN KEY (job_id) REFERENCES job_postings(id) ON DELETE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES skills(id) ON DELETE CASCADE,
    UNIQUE(job_id, skill_id)
);

CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    job_id INTEGER NOT NULL,
    status VARCHAR(30) DEFAULT 'Applied', -- Applied, Shortlisted, Rejected
    match_score INTEGER DEFAULT 0,
    applied_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (job_id) REFERENCES job_postings(id) ON DELETE CASCADE,
    UNIQUE(user_id, job_id)
);

CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    skill_id INTEGER NOT NULL,
    title VARCHAR(200) NOT NULL,
    provider VARCHAR(100) DEFAULT 'Coursera',
    source_type VARCHAR(50) NOT NULL, -- youtube, platform, company
    url VARCHAR(500) NOT NULL,
    duration VARCHAR(50) DEFAULT '4 Weeks',
    difficulty VARCHAR(50) DEFAULT 'Intermediate',
    employer_id INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (skill_id) REFERENCES skills(id) ON DELETE CASCADE,
    FOREIGN KEY (employer_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS interview_resources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    job_id INTEGER,
    title VARCHAR(200) NOT NULL,
    url VARCHAR(500) NOT NULL,
    resource_type VARCHAR(50) NOT NULL, -- Question Bank, System Design, HR Prep, Coding Prep
    description TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
    FOREIGN KEY (job_id) REFERENCES job_postings(id) ON DELETE SET NULL
);
