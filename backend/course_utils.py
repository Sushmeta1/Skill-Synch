import random

# Course database with detailed information
COURSE_DATABASE = {
    "Python": [
        {"title": "Python for Beginners", "provider": "Codecademy", "duration": "20 hours", "level": "Beginner", "rating": 4.5, "price": "Free"},
        {"title": "Advanced Python Programming", "provider": "Udemy", "duration": "40 hours", "level": "Advanced", "rating": 4.7, "price": "$89"},
        {"title": "Python Data Science", "provider": "Coursera", "duration": "60 hours", "level": "Intermediate", "rating": 4.8, "price": "$49/month"}
    ],
    "JavaScript": [
        {"title": "JavaScript Fundamentals", "provider": "freeCodeCamp", "duration": "30 hours", "level": "Beginner", "rating": 4.6, "price": "Free"},
        {"title": "Modern JavaScript ES6+", "provider": "Udemy", "duration": "25 hours", "level": "Intermediate", "rating": 4.5, "price": "$79"},
        {"title": "JavaScript Algorithms", "provider": "Pluralsight", "duration": "15 hours", "level": "Advanced", "rating": 4.4, "price": "$29/month"}
    ],
    "React": [
        {"title": "React Basics", "provider": "Meta", "duration": "35 hours", "level": "Beginner", "rating": 4.7, "price": "Free"},
        {"title": "Advanced React Patterns", "provider": "Udemy", "duration": "28 hours", "level": "Advanced", "rating": 4.6, "price": "$94"},
        {"title": "React with TypeScript", "provider": "Pluralsight", "duration": "18 hours", "level": "Intermediate", "rating": 4.5, "price": "$29/month"}
    ],
    "Node.js": [
        {"title": "Node.js Complete Guide", "provider": "Udemy", "duration": "42 hours", "level": "Beginner", "rating": 4.6, "price": "$84"},
        {"title": "Node.js Microservices", "provider": "Pluralsight", "duration": "32 hours", "level": "Advanced", "rating": 4.5, "price": "$29/month"},
        {"title": "Express.js Fundamentals", "provider": "Codecademy", "duration": "15 hours", "level": "Intermediate", "rating": 4.4, "price": "$39/month"}
    ],
    "Docker": [
        {"title": "Docker for Beginners", "provider": "Docker", "duration": "12 hours", "level": "Beginner", "rating": 4.5, "price": "Free"},
        {"title": "Docker and Kubernetes", "provider": "Udemy", "duration": "45 hours", "level": "Advanced", "rating": 4.7, "price": "$109"},
        {"title": "Container Orchestration", "provider": "Linux Academy", "duration": "25 hours", "level": "Intermediate", "rating": 4.6, "price": "$49/month"}
    ],
    "AWS": [
        {"title": "AWS Cloud Practitioner", "provider": "AWS", "duration": "20 hours", "level": "Beginner", "rating": 4.6, "price": "Free"},
        {"title": "AWS Solutions Architect", "provider": "A Cloud Guru", "duration": "60 hours", "level": "Advanced", "rating": 4.8, "price": "$39/month"},
        {"title": "AWS Developer Associate", "provider": "Udemy", "duration": "35 hours", "level": "Intermediate", "rating": 4.5, "price": "$99"}
    ],
    "Machine Learning": [
        {"title": "ML for Everyone", "provider": "Coursera", "duration": "30 hours", "level": "Beginner", "rating": 4.7, "price": "$49/month"},
        {"title": "Deep Learning Specialization", "provider": "deeplearning.ai", "duration": "120 hours", "level": "Advanced", "rating": 4.9, "price": "$49/month"},
        {"title": "Python Machine Learning", "provider": "Udemy", "duration": "40 hours", "level": "Intermediate", "rating": 4.6, "price": "$89"}
    ],
    "SQL": [
        {"title": "SQL Basics", "provider": "Codecademy", "duration": "15 hours", "level": "Beginner", "rating": 4.5, "price": "$39/month"},
        {"title": "Advanced SQL", "provider": "DataCamp", "duration": "25 hours", "level": "Advanced", "rating": 4.6, "price": "$33/month"},
        {"title": "SQL for Data Science", "provider": "Coursera", "duration": "35 hours", "level": "Intermediate", "rating": 4.7, "price": "$49/month"}
    ],
    "Git": [
        {"title": "Git & GitHub Complete Guide", "provider": "Udemy", "duration": "18 hours", "level": "Beginner", "rating": 4.5, "price": "$79"},
        {"title": "Advanced Git Workflows", "provider": "Pluralsight", "duration": "12 hours", "level": "Advanced", "rating": 4.4, "price": "$29/month"},
        {"title": "Git Version Control", "provider": "freeCodeCamp", "duration": "8 hours", "level": "Intermediate", "rating": 4.6, "price": "Free"}
    ],
    "Communication": [
        {"title": "Effective Communication", "provider": "Coursera", "duration": "20 hours", "level": "Beginner", "rating": 4.6, "price": "$49/month"},
        {"title": "Business Communication", "provider": "LinkedIn Learning", "duration": "15 hours", "level": "Intermediate", "rating": 4.5, "price": "$29/month"},
        {"title": "Public Speaking Mastery", "provider": "Udemy", "duration": "12 hours", "level": "Advanced", "rating": 4.7, "price": "$69"}
    ],
    "Leadership": [
        {"title": "Leadership Fundamentals", "provider": "LinkedIn Learning", "duration": "18 hours", "level": "Beginner", "rating": 4.6, "price": "$29/month"},
        {"title": "Strategic Leadership", "provider": "Coursera", "duration": "25 hours", "level": "Advanced", "rating": 4.7, "price": "$49/month"},
        {"title": "Team Management", "provider": "Udemy", "duration": "22 hours", "level": "Intermediate", "rating": 4.5, "price": "$79"}
    ]
}

# Learning paths for common career goals
LEARNING_PATHS = {
    "Full Stack Developer": {
        "description": "Complete pathway to become a full-stack web developer",
        "duration": "6-8 months",
        "skills": ["HTML", "CSS", "JavaScript", "React", "Node.js", "SQL", "Git"],
        "difficulty": "Intermediate"
    },
    "Data Scientist": {
        "description": "Comprehensive data science and machine learning track",
        "duration": "8-12 months", 
        "skills": ["Python", "SQL", "Machine Learning", "Statistics", "Data Visualization"],
        "difficulty": "Advanced"
    },
    "DevOps Engineer": {
        "description": "Infrastructure and deployment automation specialist",
        "duration": "4-6 months",
        "skills": ["Linux", "Docker", "Kubernetes", "AWS", "CI/CD", "Git"],
        "difficulty": "Advanced"
    },
    "Frontend Developer": {
        "description": "User interface and experience focused development",
        "duration": "4-5 months",
        "skills": ["HTML", "CSS", "JavaScript", "React", "TypeScript", "Git"],
        "difficulty": "Beginner-Intermediate"
    },
    "Backend Developer": {
        "description": "Server-side development and API design",
        "duration": "5-7 months",
        "skills": ["Python", "Node.js", "SQL", "REST API", "Docker", "Git"],
        "difficulty": "Intermediate"
    }
}

def get_course_recommendations(missing_skills, user_level="Beginner", max_courses=3):
    """
    Generate personalized course recommendations based on missing skills
    """
    recommendations = {}
    
    for skill in missing_skills[:10]:  # Limit to top 10 missing skills
        if skill in COURSE_DATABASE:
            courses = COURSE_DATABASE[skill]
            
            # Filter by user level
            suitable_courses = []
            for course in courses:
                if user_level == "Beginner" and course["level"] in ["Beginner", "Intermediate"]:
                    suitable_courses.append(course)
                elif user_level == "Intermediate" and course["level"] in ["Beginner", "Intermediate", "Advanced"]:
                    suitable_courses.append(course)
                elif user_level == "Advanced":
                    suitable_courses.append(course)
            
            # Sort by rating and select top courses
            suitable_courses.sort(key=lambda x: x["rating"], reverse=True)
            recommendations[skill] = suitable_courses[:max_courses]
    
    return recommendations

def suggest_learning_path(missing_skills, matched_skills):
    """
    Suggest complete learning paths based on skill gap analysis
    """
    suggested_paths = []
    
    for path_name, path_info in LEARNING_PATHS.items():
        path_skills = set(path_info["skills"])
        missing_from_path = path_skills - set(matched_skills)
        overlap_with_missing = len(missing_from_path.intersection(set(missing_skills)))
        
        if overlap_with_missing >= 2:  # If user is missing 2+ skills from this path
            completion_percentage = int(((len(path_skills) - len(missing_from_path)) / len(path_skills)) * 100)
            
            suggested_paths.append({
                "name": path_name,
                "description": path_info["description"],
                "duration": path_info["duration"],
                "difficulty": path_info["difficulty"],
                "completion_percentage": completion_percentage,
                "missing_skills": list(missing_from_path),
                "skills_needed": len(missing_from_path),
                "total_skills": len(path_skills)
            })
    
    # Sort by completion percentage (highest first)
    suggested_paths.sort(key=lambda x: x["completion_percentage"], reverse=True)
    return suggested_paths[:3]  # Return top 3 paths

def generate_study_plan(missing_skills, user_level="Beginner"):
    """
    Create a structured study plan with timeline
    """
    recommendations = get_course_recommendations(missing_skills, user_level)
    
    study_plan = {
        "total_duration": "0 hours",
        "estimated_completion": "2-3 months",
        "skill_priorities": [],
        "weekly_schedule": {},
        "milestones": []
    }
    
    total_hours = 0
    priority_skills = missing_skills[:6]  # Focus on top 6 missing skills
    
    for i, skill in enumerate(priority_skills):
        if skill in recommendations and recommendations[skill]:
            best_course = recommendations[skill][0]  # Take the highest rated course
            duration_hours = int(best_course["duration"].split()[0]) if best_course["duration"].split()[0].isdigit() else 20
            total_hours += duration_hours
            
            study_plan["skill_priorities"].append({
                "skill": skill,
                "priority": i + 1,
                "course": best_course["title"],
                "duration": best_course["duration"],
                "provider": best_course["provider"],
                "estimated_weeks": max(1, duration_hours // 10)  # Assuming 10 hours per week
            })
    
    study_plan["total_duration"] = f"{total_hours} hours"
    study_plan["estimated_completion"] = f"{max(1, total_hours // 40)}-{max(2, total_hours // 30)} months"
    
    # Create weekly schedule
    weeks = max(1, total_hours // 10)
    study_plan["weekly_schedule"] = {
        "hours_per_week": 10,
        "total_weeks": weeks,
        "suggested_split": "70% hands-on coding, 30% theory"
    }
    
    # Generate milestones
    study_plan["milestones"] = [
        {"week": max(1, weeks // 4), "goal": "Complete first priority skill"},
        {"week": max(2, weeks // 2), "goal": "Build first project using new skills"},
        {"week": max(3, (3 * weeks) // 4), "goal": "Complete advanced topics"},
        {"week": weeks, "goal": "Portfolio project and skill assessment"}
    ]
    
    return study_plan

def get_skill_market_insights(skills):
    """
    Provide market insights for skills (simulated data)
    """
    # Simulated market data
    market_data = {
        "Python": {"demand": "Very High", "avg_salary": "$95,000", "growth": "+15%"},
        "JavaScript": {"demand": "Very High", "avg_salary": "$88,000", "growth": "+12%"},
        "React": {"demand": "High", "avg_salary": "$92,000", "growth": "+18%"},
        "Node.js": {"demand": "High", "avg_salary": "$89,000", "growth": "+14%"},
        "AWS": {"demand": "Very High", "avg_salary": "$110,000", "growth": "+22%"},
        "Docker": {"demand": "High", "avg_salary": "$95,000", "growth": "+20%"},
        "Machine Learning": {"demand": "Very High", "avg_salary": "$125,000", "growth": "+25%"},
        "SQL": {"demand": "High", "avg_salary": "$75,000", "growth": "+8%"},
        "Git": {"demand": "Medium", "avg_salary": "$80,000", "growth": "+5%"},
        "Communication": {"demand": "High", "avg_salary": "+$10,000", "growth": "+8%"},
        "Leadership": {"demand": "High", "avg_salary": "+$15,000", "growth": "+10%"}
    }
    
    insights = {}
    for skill in skills[:5]:  # Top 5 skills
        if skill in market_data:
            insights[skill] = market_data[skill]
        else:
            insights[skill] = {"demand": "Medium", "avg_salary": "$70,000", "growth": "+6%"}
    
    return insights

def generate_complete_learning_report(missing_skills, matched_skills, user_level="Beginner"):
    """
    Generate a comprehensive learning and career development report
    """
    course_recommendations = get_course_recommendations(missing_skills, user_level)
    learning_paths = suggest_learning_path(missing_skills, matched_skills)
    study_plan = generate_study_plan(missing_skills, user_level)
    market_insights = get_skill_market_insights(missing_skills)
    
    return {
        "course_recommendations": course_recommendations,
        "suggested_learning_paths": learning_paths,
        "personalized_study_plan": study_plan,
        "market_insights": market_insights,
        "summary": {
            "total_missing_skills": len(missing_skills),
            "courses_available": sum(len(courses) for courses in course_recommendations.values()),
            "recommended_learning_paths": len(learning_paths),
            "estimated_upskilling_time": study_plan["estimated_completion"]
        }
    }
