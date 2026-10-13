from database import sqlite_db
from datetime import datetime
import json

def seed_database():
    conn = sqlite_db.get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM users")
    if cur.fetchone()[0] > 0:
        print("[Seed] SQLite database already contains data. Skipping.")
        conn.close()
        return
    print("[Seed] Seeding data into SQLite...")
    
    # Companies
    companies = [
        (1,"Google","Product-Based IT","Mountain View, CA / Remote","https://img.icons8.com/color/144/google-logo.png","Global tech giant","https://careers.google.com"),
        (2,"Microsoft","Product-Based IT","Redmond, WA / Hybrid","https://img.icons8.com/color/144/microsoft.png","Cloud & AI","https://careers.microsoft.com"),
        (3,"Meta","Product-Based IT","Menlo Park, CA / Remote","https://img.icons8.com/color/144/meta.png","Social/AI","https://metacareers.com"),
    ]
    for c in companies:
        cur.execute("INSERT OR REPLACE INTO companies (id,name,industry,location,logo_url,description,website) VALUES (?,?,?,?,?,?,?)", 
                   (str(c[0]), c[1], c[2], c[3], c[4], c[5], c[6]))
    
    # Skills
    skills = [
        (1,"Python","Programming"),
        (2,"JavaScript","Programming"),
        (3,"Machine Learning","AI/ML"),
        (4,"Data Structures & Algorithms","Core"),
        (5,"System Design","Core"),
        (6,"React","Frontend"),
        (7,"Node.js","Backend"),
        (8,"Docker","DevOps"),
        (9,"AWS","Cloud"),
        (10,"SQL","Database"),
    ]
    for s in skills:
        cur.execute("INSERT OR REPLACE INTO skills (id,name,category) VALUES (?,?,?)", (str(s[0]), s[1], s[2]))
    
    # Jobs
    jobs = [
        (1,1,"Software Engineer","SDE","3-5 Years","Remote","15-30 LPA","Join Google engineering team."),
        (2,2,"ML Engineer","ML","2-4 Years","Hybrid","12-25 LPA","Build AI features."),
        (3,3,"Backend Engineer","Backend","2-5 Years","Remote","14-28 LPA","Scale backend systems."),
    ]
    for j in jobs:
        cur.execute("INSERT OR REPLACE INTO job_postings (id,company_id,title,domain,experience_required,location,salary_range,description,created_at) VALUES (?,?,?,?,?,?,?,?,?)",
                   (str(j[0]), str(j[1]), j[2], j[3], j[4], j[5], j[6], j[7], datetime.utcnow().isoformat()))
    
    # Courses
    courses = [
        (1,1,"Python Complete Course","Udemy","platform","https://example.com","40 Hours","Beginner"),
        (2,2,"JavaScript Essentials","Coursera","platform","https://example.com","30 Hours","Beginner"),
        (3,3,"ML Crash Course","Google","platform","https://example.com","25 Hours","Intermediate"),
    ]
    for c in courses:
        cur.execute("INSERT OR REPLACE INTO courses (id,skill_id,title,provider,source_type,url,duration,difficulty,created_at) VALUES (?,?,?,?,?,?,?,?,?)",
                   (str(c[0]), str(c[1]), c[2], c[3], c[4], c[5], c[6], c[7], datetime.utcnow().isoformat()))
    
    conn.commit()
    conn.close()
    print("[Seed] Done.")
