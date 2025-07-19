import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
import re

# Load environment variables
load_dotenv()

# Initialize Gemini AI
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        
        # Try different model names based on availability
        model_names = [
            'gemini-1.5-flash',
            'gemini-1.5-pro',
            'gemini-pro',
            'models/gemini-1.5-flash',
            'models/gemini-1.5-pro',
            'models/gemini-pro'
        ]
        
        model = None
        for model_name in model_names:
            try:
                model = genai.GenerativeModel(model_name)
                # Test the model with a simple prompt
                test_response = model.generate_content("Hello")
                print(f"✅ Gemini AI initialized successfully with model: {model_name}")
                AI_ENABLED = True
                break
            except Exception as e:
                print(f"⚠️  Model {model_name} not available: {e}")
                continue
        
        if not model:
            print("❌ No compatible Gemini models found. Using fallback mode.")
            AI_ENABLED = False
        
    except Exception as e:
        print(f"❌ Gemini AI initialization failed: {e}")
        AI_ENABLED = False
else:
    AI_ENABLED = False
    print("⚠️  Gemini API key not found. Set GEMINI_API_KEY environment variable for AI features.")

def generate_ai_resume_feedback(resume_data, job_description, user_level="Intermediate"):
    """
    Generate intelligent, personalized resume feedback using Gemini AI
    """
    if not AI_ENABLED:
        return generate_fallback_resume_feedback(resume_data)
    
    try:
        prompt = f"""
        As an expert career coach and HR professional, analyze this resume against the job description and provide detailed, actionable feedback.

        **Job Description:**
        {job_description}

        **Resume Analysis Data:**
        - Overall Match Score: {resume_data.get('similarity_score', 0)}%
        - Experience Level: {user_level}
        - Matched Skills: {', '.join(resume_data.get('matched_skills', []))}
        - Missing Skills: {', '.join(resume_data.get('missing_skills', []))}
        - Technical Skills Found: {', '.join(resume_data.get('skill_categories', {}).get('Technical', []))}
        - Soft Skills Found: {', '.join(resume_data.get('skill_categories', {}).get('Soft Skills', []))}

        Please provide:

        1. **Overall Assessment** (2-3 sentences about the resume's strength for this position)

        2. **Top 3 Strengths** (specific skills/experiences that align well)

        3. **Critical Gaps** (3-4 most important missing elements)

        4. **Resume Optimization Tips** (5 specific, actionable improvements)

        5. **Industry-Specific Advice** (2-3 insights based on the job's industry/role)

        6. **Next Steps** (3 concrete actions to take)

        Format your response as JSON with keys: overall_assessment, strengths, critical_gaps, optimization_tips, industry_advice, next_steps
        Each section should be an array of strings except overall_assessment which should be a single string.
        """

        # Retry logic for API calls
        for attempt in range(3):
            try:
                response = model.generate_content(prompt)
                ai_feedback = parse_ai_response(response.text)
                
                return {
                    "ai_powered": True,
                    "feedback_type": "comprehensive_analysis",
                    **ai_feedback
                }
            except Exception as api_error:
                print(f"AI API attempt {attempt + 1} failed: {api_error}")
                if attempt == 2:  # Last attempt
                    raise api_error
                
        return generate_fallback_resume_feedback(resume_data)
        
    except Exception as e:
        print(f"AI feedback generation error: {e}")
        return generate_fallback_resume_feedback(resume_data)

def generate_ai_interview_feedback(interview_data, transcript=""):
    """
    Generate intelligent interview performance feedback using Gemini AI
    """
    if not AI_ENABLED:
        return generate_fallback_interview_feedback(interview_data)
    
    try:
        prompt = f"""
        As an expert interview coach and communication specialist, analyze this interview performance and provide detailed, personalized feedback.

        **Interview Performance Data:**
        - Overall Score: {interview_data.get('overall_score', 0)}%
        - Confidence Score: {interview_data.get('speech_analysis', {}).get('confidence_score', 0)}%
        - Clarity Score: {interview_data.get('speech_analysis', {}).get('clarity_score', 0)}%
        - Hesitation Rate: {interview_data.get('speech_analysis', {}).get('hesitation_rate', 0)}%
        - Content Quality: {interview_data.get('content_analysis', {}).get('content_quality_score', 0)}%
        - Technical Skills Mentioned: {', '.join(interview_data.get('content_analysis', {}).get('technical_skills_mentioned', []))}
        - Soft Skills Mentioned: {', '.join(interview_data.get('content_analysis', {}).get('soft_skills_mentioned', []))}
        - Dominant Emotion: {interview_data.get('sentiment_analysis', {}).get('dominant_emotion', 'neutral')}

        **Interview Transcript:**
        "{transcript[:1000]}..." (truncated if longer)

        Please provide:

        1. **Performance Summary** (2-3 sentences highlighting overall interview performance)

        2. **Communication Strengths** (3-4 specific positive aspects of their communication)

        3. **Areas for Improvement** (4-5 specific areas to work on with explanations)

        4. **Technical Response Quality** (assessment of technical knowledge demonstration)

        5. **Soft Skills Assessment** (evaluation of interpersonal and professional skills shown)

        6. **Interview Strategies** (5 specific techniques to improve future performance)

        7. **Practice Recommendations** (3-4 concrete exercises or activities)

        Format your response as JSON with keys: performance_summary, communication_strengths, areas_for_improvement, technical_response_quality, soft_skills_assessment, interview_strategies, practice_recommendations
        Each section should be an array of strings except performance_summary and technical_response_quality which should be single strings.
        """

        response = model.generate_content(prompt)
        ai_feedback = parse_ai_response(response.text)
        
        return {
            "ai_powered": True,
            "feedback_type": "comprehensive_interview_analysis",
            **ai_feedback
        }
        
    except Exception as e:
        print(f"AI interview feedback error: {e}")
        return generate_fallback_interview_feedback(interview_data)

def generate_ai_career_insights(missing_skills, matched_skills, user_level="Intermediate"):
    """
    Generate intelligent career development insights and personalized learning paths
    """
    if not AI_ENABLED:
        return generate_fallback_career_insights(missing_skills, matched_skills)
    
    try:
        prompt = f"""
        As a career development expert and industry analyst, provide personalized career insights and learning recommendations.

        **Current Skill Profile:**
        - Experience Level: {user_level}
        - Current Skills: {', '.join(matched_skills)}
        - Missing/Desired Skills: {', '.join(missing_skills)}

        Please provide:

        1. **Career Trajectory Analysis** (2-3 sentences about their current position and potential paths)

        2. **Skill Prioritization** (rank the missing skills by importance and market demand)

        3. **Industry Trends** (3-4 relevant trends affecting these skills)

        4. **Learning Strategy** (personalized approach based on their experience level)

        5. **Timeline Recommendations** (realistic timeline for skill development)

        6. **Market Opportunities** (specific roles/companies that value these skills)

        7. **Networking Advice** (how to leverage current skills while building new ones)

        Format your response as JSON with keys: career_trajectory_analysis, skill_prioritization, industry_trends, learning_strategy, timeline_recommendations, market_opportunities, networking_advice
        Each section should be an array of strings except career_trajectory_analysis and learning_strategy which should be single strings.
        """

        response = model.generate_content(prompt)
        ai_insights = parse_ai_response(response.text)
        
        return {
            "ai_powered": True,
            "insight_type": "career_development_analysis",
            **ai_insights
        }
        
    except Exception as e:
        print(f"AI career insights error: {e}")
        return generate_fallback_career_insights(missing_skills, matched_skills)

def generate_personalized_course_recommendations(missing_skills, user_level, career_goals=""):
    """
    Generate AI-powered, personalized course recommendations beyond the basic database
    """
    if not AI_ENABLED:
        return {"ai_powered": False, "recommendations": []}
    
    try:
        prompt = f"""
        As a learning and development specialist, recommend the best courses and learning resources for this person.

        **Learner Profile:**
        - Experience Level: {user_level}
        - Skills to Develop: {', '.join(missing_skills[:5])}
        - Career Goals: {career_goals or 'Professional advancement in tech'}

        For each of the top 3 skills they need to develop, recommend:
        1. **Best Overall Course** (most comprehensive)
        2. **Quick Start Option** (fastest way to get basic proficiency)
        3. **Advanced/Specialized** (for deep expertise)
        4. **Free Alternative** (budget-friendly option)
        5. **Learning Strategy** (how to approach learning this skill)

        Format as JSON with key "skill_recommendations" containing an array of objects with:
        {
            "skill": "skill_name",
            "best_overall": {"title": "", "provider": "", "reason": ""},
            "quick_start": {"title": "", "provider": "", "reason": ""},
            "advanced": {"title": "", "provider": "", "reason": ""},
            "free_alternative": {"title": "", "provider": "", "reason": ""},
            "learning_strategy": "specific approach for this skill"
        }
        """

        response = model.generate_content(prompt)
        ai_recommendations = parse_ai_response(response.text)
        
        return {
            "ai_powered": True,
            "personalized": True,
            **ai_recommendations
        }
        
    except Exception as e:
        print(f"AI course recommendations error: {e}")
        return {"ai_powered": False, "recommendations": []}

def parse_ai_response(response_text):
    """
    Parse AI response and extract JSON content safely
    """
    try:
        # Try to find JSON in the response
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            json_str = json_match.group()
            return json.loads(json_str)
        else:
            # If no JSON found, try to parse the whole response
            return json.loads(response_text)
    except json.JSONDecodeError:
        # If JSON parsing fails, create structured response from text
        return parse_text_to_structured_response(response_text)

def parse_text_to_structured_response(text):
    """
    Convert unstructured AI response to structured format
    """
    sections = {}
    current_section = None
    current_content = []
    
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check if this is a section header
        if any(keyword in line.lower() for keyword in ['assessment', 'strengths', 'gaps', 'tips', 'advice', 'steps', 'summary', 'improvement']):
            if current_section:
                sections[current_section] = current_content
            current_section = line.lower().replace(' ', '_').replace(':', '')
            current_content = []
        elif line.startswith(('•', '-', '*', '1.', '2.', '3.')):
            # This is a list item
            content = re.sub(r'^[\•\-\*\d\.]\s*', '', line)
            current_content.append(content)
        elif current_section:
            # This is continuation of current section
            if current_content:
                current_content[-1] += ' ' + line
            else:
                current_content.append(line)
    
    # Add the last section
    if current_section:
        sections[current_section] = current_content
    
    return sections

# Fallback functions for when AI is not available
def generate_fallback_resume_feedback(resume_data):
    """Fallback resume feedback when AI is not available"""
    score = resume_data.get('similarity_score', 0)
    missing_count = len(resume_data.get('missing_skills', []))
    
    return {
        "ai_powered": False,
        "overall_assessment": f"Your resume shows a {score}% match with the job requirements. {'Strong alignment!' if score > 75 else 'Good foundation with room for improvement.' if score > 50 else 'Significant gaps to address.'}",
        "strengths": [
            f"Successfully demonstrates {len(resume_data.get('matched_skills', []))} relevant skills",
            "Shows experience in key technical areas",
            "Includes both technical and soft skills"
        ],
        "critical_gaps": [f"Missing {missing_count} key skills from job requirements"] + resume_data.get('missing_skills', [])[:3],
        "optimization_tips": [
            "Add specific examples of your achievements",
            "Quantify your impact with numbers and metrics",
            "Tailor your resume keywords to match the job description",
            "Highlight relevant projects and experiences",
            "Include industry-specific terminology"
        ],
        "industry_advice": [
            "Focus on demonstrating hands-on experience",
            "Keep up with current industry trends and technologies"
        ],
        "next_steps": [
            "Complete courses in missing skill areas",
            "Build portfolio projects showcasing new skills",
            "Network with professionals in your target role"
        ]
    }

def generate_fallback_interview_feedback(interview_data):
    """Fallback interview feedback when AI is not available"""
    score = interview_data.get('overall_score', 0)
    
    return {
        "ai_powered": False,
        "performance_summary": f"Overall interview performance score of {score}%. {'Excellent performance!' if score > 80 else 'Good performance with areas for improvement.' if score > 60 else 'Focus on building confidence and preparation.'}",
        "communication_strengths": [
            "Clear verbal communication",
            "Professional demeanor",
            "Relevant technical knowledge"
        ],
        "areas_for_improvement": [
            "Reduce filler words and hesitation",
            "Provide more specific examples",
            "Improve confidence in responses",
            "Better structure for answers"
        ],
        "interview_strategies": [
            "Practice the STAR method for behavioral questions",
            "Prepare specific examples for each skill",
            "Research company culture and values",
            "Practice technical explanations",
            "Work on body language and eye contact"
        ]
    }

def generate_fallback_career_insights(missing_skills, matched_skills):
    """Fallback career insights when AI is not available"""
    return {
        "ai_powered": False,
        "career_trajectory_analysis": "Based on your current skills and market trends, you're well-positioned for growth in the technology sector.",
        "skill_prioritization": missing_skills[:5],  # Top 5 missing skills
        "industry_trends": [
            "Increasing demand for cloud computing skills",
            "AI and machine learning integration in most roles",
            "Remote work driving collaboration tool expertise",
            "Emphasis on continuous learning and adaptability"
        ],
        "learning_strategy": "Focus on building one new skill at a time through hands-on projects and practical application.",
        "market_opportunities": [
            "Full-stack development roles",
            "Cloud engineering positions",
            "DevOps and automation specialists",
            "Data science and analytics roles"
        ]
    } 