# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import os
# from werkzeug.utils import secure_filename
# from resume_utils import match_resume_to_job
# from interview_utils import analyze_interview_audio  # Import moved to the top

# app = Flask(__name__)
# CORS(app)

# # Upload folder config
# UPLOAD_FOLDER = 'uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # Create the uploads folder if it doesn't exist
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# # Root route (optional)
# @app.route('/')
# def index():
#     return "✅ SkillSync Resume Analysis Server is Running!"

# # Resume analysis route
# @app.route('/analyze-resume', methods=['POST'])
# def analyze_resume():
#     if 'resume' not in request.files or 'job_description' not in request.form:
#         return jsonify({'error': 'Missing resume or job description'}), 400

#     resume_file = request.files['resume']
#     job_description = request.form['job_description']

#     if resume_file.filename == '':
#         return jsonify({'error': 'No resume file selected'}), 400

#     filename = secure_filename(resume_file.filename)
#     file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#     resume_file.save(file_path)

#     # Call utility function to analyze resume
#     result = match_resume_to_job(file_path, job_description)

#     # Clean up uploaded file
#     os.remove(file_path)

#     return jsonify(result)

# # Interview audio analysis route
# @app.route('/analyze-interview', methods=['POST'])
# def analyze_interview():
#     if 'interview' not in request.files:
#         return jsonify({'error': 'Missing interview file'}), 400

#     interview_file = request.files['interview']

#     if interview_file.filename == '':
#         return jsonify({'error': 'No interview file selected'}), 400

#     filename = secure_filename(interview_file.filename)
#     file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#     interview_file.save(file_path)

#     result = analyze_interview_audio(file_path)

#     # Clean up
#     os.remove(file_path)
#     return jsonify(result)

# # Server runner
# if __name__ == '__main__':
#     print("✅ SkillSync backend running on http://127.0.0.1:5000")
#     app.run(debug=True)

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import time
from werkzeug.utils import secure_filename

from resume_utils import match_resume_to_job
from interview_utils import analyze_interview  # ✅ Correct import
from course_utils import generate_complete_learning_report, get_course_recommendations
from ai_utils import generate_ai_resume_feedback, generate_ai_interview_feedback, generate_ai_career_insights

app = Flask(__name__)
CORS(app)

# Upload folder configuration
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ============================
# ✅ Root Route (optional)
# ============================
@app.route('/')
def index():
    return "✅ SkillSync Backend is Running!"

# ============================
# 📄 Resume Analysis Endpoint
# ============================
@app.route('/analyze-resume', methods=['POST'])
def analyze_resume():
    if 'resume' not in request.files or 'job_description' not in request.form:
        return jsonify({'error': 'Missing resume or job description'}), 400

    resume_file = request.files['resume']
    job_description = request.form['job_description']
    user_level = request.form.get('user_level', 'Beginner')  # Optional user level

    if resume_file.filename == '':
        return jsonify({'error': 'No resume file selected'}), 400

    filename = secure_filename(resume_file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    resume_file.save(file_path)

    # Get resume analysis
    result = match_resume_to_job(file_path, job_description)
    
    # Generate AI-powered feedback
    ai_feedback = generate_ai_resume_feedback(result, job_description, user_level)
    
    # Generate course recommendations with AI insights
    learning_report = generate_complete_learning_report(
        result['missing_skills'], 
        result['matched_skills'], 
        user_level
    )
    
    # Generate career insights
    career_insights = generate_ai_career_insights(
        result['missing_skills'],
        result['matched_skills'],
        user_level
    )
    
    # Combine results
    result['ai_feedback'] = ai_feedback
    result['learning_recommendations'] = learning_report
    result['career_insights'] = career_insights

    os.remove(file_path)
    return jsonify(result)

# ================================
# 🎤 Interview Analysis Endpoint (Audio & Video)
# ================================
@app.route('/analyze-interview', methods=['POST'])
def analyze_interview_route():  # ✅ Renamed to avoid name clash
    if 'interview' not in request.files:
        return jsonify({'error': 'Missing interview file'}), 400

    interview_file = request.files['interview']
    if interview_file.filename == '':
        return jsonify({'error': 'No interview file selected'}), 400

    filename = secure_filename(interview_file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    try:
        interview_file.save(file_path)
        
        # Check file type for better error messages
        file_ext = filename.lower().split('.')[-1]
        supported_audio = ['mp3', 'wav', 'm4a', 'aac', 'ogg']
        supported_video = ['mp4', 'avi', 'mov', 'mkv', 'webm', 'flv', 'wmv', 'm4v']
        
        if file_ext not in supported_audio + supported_video:
            os.remove(file_path)
            return jsonify({
                'error': f'Unsupported file format: .{file_ext}',
                'supported_formats': {
                    'audio': supported_audio,
                    'video': supported_video
                }
            }), 400
        
        print(f"🎬 Processing {'video' if file_ext in supported_video else 'audio'} file: {filename}")
        
        # Analyze interview (supports both audio and video)
        result = analyze_interview(file_path)
        
        # Generate AI-powered interview feedback
        ai_feedback = generate_ai_interview_feedback(
            result, 
            result.get('transcript', '')
        )
        
        # Add AI feedback to result
        result['ai_feedback'] = ai_feedback
        
        # Add processing metadata
        result['processing_info'] = {
            'original_filename': filename,
            'file_type': 'video' if file_ext in supported_video else 'audio',
            'file_format': file_ext,
            'processing_timestamp': int(time.time()) if 'time' in globals() else None
        }
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Interview analysis error: {e}")
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500
        
    finally:
        # Clean up uploaded file
        if os.path.exists(file_path):
            os.remove(file_path)

# ===============================
# 📚 Course Recommendations API
# ===============================
@app.route('/get-courses', methods=['POST'])
def get_courses():
    data = request.get_json()
    
    if not data or 'missing_skills' not in data:
        return jsonify({'error': 'Missing skills data'}), 400
    
    missing_skills = data['missing_skills']
    matched_skills = data.get('matched_skills', [])
    user_level = data.get('user_level', 'Beginner')
    
    learning_report = generate_complete_learning_report(missing_skills, matched_skills, user_level)
    
    return jsonify(learning_report)

# ============================
# 📊 Analytics Endpoint
# ============================
@app.route('/get-analytics', methods=['GET'])
def get_analytics():
    # Mock analytics data - in a real app, this would come from a database
    analytics = {
        "user_progress": {
            "total_analyses": 15,
            "resume_analyses": 10,
            "interview_analyses": 5,
            "average_improvement": 23,
            "skills_learned": 8
        },
        "skill_trends": {
            "most_requested": ["Python", "JavaScript", "React", "AWS", "Docker"],
            "fastest_growing": ["Machine Learning", "Docker", "Kubernetes", "React", "TypeScript"],
            "market_demand": {
                "Python": 95,
                "JavaScript": 92,
                "React": 88,
                "AWS": 85,
                "Docker": 82
            }
        },
        "performance_metrics": {
            "average_resume_score": 72,
            "average_interview_score": 76,
            "improvement_rate": 15,
            "completion_rate": 85
        },
        "recent_activity": [
            {"date": "2024-01-15", "type": "resume", "score": 78, "skills_gap": 5},
            {"date": "2024-01-12", "type": "interview", "score": 82, "improvement": 12},
            {"date": "2024-01-10", "type": "resume", "score": 65, "skills_gap": 8},
            {"date": "2024-01-08", "type": "interview", "score": 70, "improvement": 8},
            {"date": "2024-01-05", "type": "resume", "score": 68, "skills_gap": 6}
        ]
    }
    
    return jsonify(analytics)

# ============================
# 🔁 Run the Server
# ============================
if __name__ == '__main__':
    print("✅ SkillSync backend running on http://127.0.0.1:5000")
    app.run(debug=True)
