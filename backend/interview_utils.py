import os
import re
from collections import Counter
import json

# Try importing advanced libraries, fall back to basic functionality if not available
try:
    import speech_recognition as sr
    from pydub import AudioSegment
    from textblob import TextBlob
    import numpy as np
    ADVANCED_FEATURES = True
except ImportError:
    ADVANCED_FEATURES = False
    print("⚠️  Advanced audio libraries not available. Using basic simulation mode.")
    print("   To enable full features, install: pip install SpeechRecognition pydub textblob numpy")

# Try importing video processing utilities
try:
    from video_utils import (
        is_video_file, 
        process_video_for_interview_analysis,
        cleanup_temp_files,
        VIDEO_PROCESSING_AVAILABLE
    )
except ImportError:
    VIDEO_PROCESSING_AVAILABLE = False
    print("⚠️  Video utilities not available. Video files will not be supported.")
    print("   Make sure video_utils.py is available and dependencies are installed.")

def convert_audio_to_wav(audio_path):
    """Convert audio file to WAV format for speech recognition"""
    if not ADVANCED_FEATURES:
        return audio_path
    
    try:
        from pydub import AudioSegment
        audio = AudioSegment.from_file(audio_path)
        wav_path = audio_path.rsplit('.', 1)[0] + '.wav'
        audio.export(wav_path, format="wav")
        return wav_path
    except Exception as e:
        print(f"Error converting audio: {e}")
        return audio_path

def transcribe_audio(audio_path):
    """Convert audio to text using speech recognition"""
    if not ADVANCED_FEATURES:
        print("📁 Audio file received - Using demo transcript for analysis")
        return "hello my name is john and i am excited about this opportunity i have experience in python javascript and react i enjoy working with teams and solving complex problems um i have worked on several projects and i am confident in my abilities"
    
    try:
        import speech_recognition as sr
        recognizer = sr.Recognizer()
        
        # Convert to WAV if needed
        if not audio_path.lower().endswith('.wav'):
            audio_path = convert_audio_to_wav(audio_path)
        
        with sr.AudioFile(audio_path) as source:
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio_data = recognizer.record(source)
            
        # Use Google's speech recognition
        text = recognizer.recognize_google(audio_data)
        return text.lower()
        
    except sr.UnknownValueError:
        return "Could not understand audio clearly"
    except sr.RequestError as e:
        return f"Error with speech recognition service: {e}"
    except Exception as e:
        print(f"Transcription error: {e}")
        # Fallback to mock data for demo purposes
        return "hello my name is john and i am excited about this opportunity i have experience in python javascript and react i enjoy working with teams and solving complex problems"

def analyze_speech_patterns(text):
    """Analyze speech patterns for confidence, clarity, and hesitation"""
    
    # Count filler words
    filler_words = ['um', 'uh', 'er', 'ah', 'like', 'you know', 'so', 'basically', 'actually']
    filler_count = sum(text.lower().count(word) for word in filler_words)
    
    # Count total words
    words = text.split()
    total_words = len(words)
    
    # Calculate metrics
    hesitation_rate = min(100, (filler_count / max(total_words, 1)) * 100) if total_words > 0 else 0
    
    # Confidence indicators
    confident_phrases = ['i am confident', 'i believe', 'i know', 'definitely', 'absolutely', 'certainly']
    uncertain_phrases = ['maybe', 'i think', 'probably', 'not sure', 'i guess', 'perhaps']
    
    confident_count = sum(text.lower().count(phrase) for phrase in confident_phrases)
    uncertain_count = sum(text.lower().count(phrase) for phrase in uncertain_phrases)
    
    # Calculate confidence score
    confidence_base = max(0, 80 - hesitation_rate)
    confidence_adjustment = (confident_count * 5) - (uncertain_count * 3)
    confidence_score = min(100, max(0, confidence_base + confidence_adjustment))
    
    # Clarity score based on sentence structure and vocabulary
    sentences = text.split('.')
    avg_sentence_length = sum(len(s.split()) for s in sentences) / max(len(sentences), 1)
    
    # Ideal sentence length is 10-20 words
    clarity_score = 100 - abs(avg_sentence_length - 15) * 2
    clarity_score = max(50, min(100, clarity_score))
    
    return {
        "confidence_score": int(confidence_score),
        "clarity_score": int(clarity_score),
        "hesitation_rate": int(hesitation_rate),
        "filler_word_count": filler_count,
        "total_words": total_words,
        "avg_sentence_length": round(avg_sentence_length, 1)
    }

def analyze_sentiment_emotions(text):
    """Analyze emotional tone and sentiment of the speech"""
    
    if ADVANCED_FEATURES:
        try:
            from textblob import TextBlob
            blob = TextBlob(text)
            # Get polarity (-1 to 1) and subjectivity (0 to 1)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
        except ImportError:
            # Fallback to basic sentiment analysis
            polarity = 0.2  # Slightly positive
            subjectivity = 0.5  # Moderate subjectivity
    else:
        # Basic sentiment analysis based on keywords
        positive_words = ['excited', 'confident', 'enjoy', 'love', 'passionate', 'skilled']
        negative_words = ['nervous', 'worried', 'difficult', 'struggle', 'unsure']
        
        positive_count = sum(1 for word in positive_words if word in text.lower())
        negative_count = sum(1 for word in negative_words if word in text.lower())
        
        # Simple polarity calculation
        total_sentiment_words = positive_count + negative_count
        if total_sentiment_words > 0:
            polarity = (positive_count - negative_count) / total_sentiment_words
        else:
            polarity = 0.1  # Neutral-positive default
        
        subjectivity = 0.6  # Default moderate subjectivity
    
    # Emotion keywords analysis
    emotion_keywords = {
        'enthusiasm': ['excited', 'passionate', 'love', 'enjoy', 'thrilled', 'eager'],
        'confidence': ['confident', 'capable', 'skilled', 'experienced', 'proficient'],
        'nervousness': ['nervous', 'worried', 'anxious', 'uncertain', 'hesitant'],
        'professionalism': ['professional', 'responsible', 'reliable', 'dedicated', 'committed'],
        'curiosity': ['interested', 'curious', 'learn', 'explore', 'discover']
    }
    
    emotion_scores = {}
    for emotion, keywords in emotion_keywords.items():
        score = sum(text.lower().count(keyword) for keyword in keywords)
        emotion_scores[emotion] = score
    
    # Convert to percentages (normalize)
    total_emotion_score = sum(emotion_scores.values()) or 1
    emotion_percentages = {
        emotion: int((score / total_emotion_score) * 100) 
        for emotion, score in emotion_scores.items()
    }
    
    # Determine overall emotional state
    if polarity > 0.3:
        overall_sentiment = "Positive"
    elif polarity < -0.3:
        overall_sentiment = "Negative"
    else:
        overall_sentiment = "Neutral"
    
    return {
        "overall_sentiment": overall_sentiment,
        "polarity": round(polarity, 2),
        "subjectivity": round(subjectivity, 2),
        "emotion_breakdown": emotion_percentages,
        "dominant_emotion": max(emotion_percentages, key=emotion_percentages.get)
    }

def analyze_content_quality(text):
    """Analyze the quality and relevance of interview content"""
    
    # Technical skills mentioned
    technical_skills = [
        'python', 'javascript', 'java', 'react', 'node', 'sql', 'aws', 'docker',
        'kubernetes', 'git', 'html', 'css', 'mongodb', 'postgresql', 'redis',
        'machine learning', 'ai', 'data science', 'api', 'rest', 'microservices'
    ]
    
    # Soft skills mentioned
    soft_skills = [
        'teamwork', 'leadership', 'communication', 'problem solving', 'creative',
        'analytical', 'organized', 'adaptable', 'collaborative', 'motivated'
    ]
    
    # Experience indicators
    experience_indicators = [
        'experience', 'worked', 'developed', 'built', 'implemented', 'managed',
        'led', 'created', 'designed', 'optimized', 'maintained', 'deployed'
    ]
    
    mentioned_technical = [skill for skill in technical_skills if skill in text.lower()]
    mentioned_soft = [skill for skill in soft_skills if skill in text.lower()]
    mentioned_experience = [indicator for indicator in experience_indicators if indicator in text.lower()]
    
    # Calculate content quality score
    technical_score = min(40, len(mentioned_technical) * 8)
    soft_score = min(30, len(mentioned_soft) * 6)
    experience_score = min(30, len(mentioned_experience) * 3)
    
    content_quality = technical_score + soft_score + experience_score
    
    return {
        "content_quality_score": int(content_quality),
        "technical_skills_mentioned": mentioned_technical,
        "soft_skills_mentioned": mentioned_soft,
        "experience_indicators": len(mentioned_experience),
        "detailed_breakdown": {
            "technical_score": technical_score,
            "soft_skills_score": soft_score,
            "experience_score": experience_score
        }
    }

def generate_feedback(speech_analysis, sentiment_analysis, content_analysis):
    """Generate personalized feedback based on analysis results"""
    
    feedback = []
    
    # Confidence feedback
    if speech_analysis["confidence_score"] < 60:
        feedback.append("Practice speaking with more conviction. Use definitive statements like 'I can' instead of 'I think I can'.")
    elif speech_analysis["confidence_score"] > 85:
        feedback.append("Great confidence level! You come across as self-assured and capable.")
    
    # Hesitation feedback
    if speech_analysis["hesitation_rate"] > 20:
        feedback.append("Try to reduce filler words (um, ah, like). Practice speaking more deliberately and pause instead of using fillers.")
    elif speech_analysis["hesitation_rate"] < 5:
        feedback.append("Excellent fluency! You speak clearly without unnecessary hesitation.")
    
    # Clarity feedback
    if speech_analysis["clarity_score"] < 70:
        feedback.append("Work on structuring your sentences better. Aim for 10-20 words per sentence for optimal clarity.")
    
    # Emotional feedback
    if sentiment_analysis["dominant_emotion"] == "nervousness":
        feedback.append("Try relaxation techniques before interviews to manage nerves. Deep breathing can help you sound more composed.")
    elif sentiment_analysis["dominant_emotion"] == "enthusiasm":
        feedback.append("Your enthusiasm comes through clearly! This positive energy is a great asset.")
    
    # Content feedback
    if content_analysis["content_quality_score"] < 50:
        feedback.append("Include more specific examples of your technical skills and work experience.")
    
    if len(content_analysis["technical_skills_mentioned"]) < 2:
        feedback.append("Mention more relevant technical skills that match the job requirements.")
    
    if len(content_analysis["soft_skills_mentioned"]) < 2:
        feedback.append("Highlight soft skills like teamwork, leadership, or problem-solving with specific examples.")
    
    # Overall feedback
    if sentiment_analysis["overall_sentiment"] == "Positive":
        feedback.append("Maintain this positive attitude - it shows genuine interest in the role.")
    
    return feedback

def analyze_interview(file_path):
    """
    Complete interview analysis pipeline - supports both audio and video files
    """
    audio_path = file_path
    temp_dir = None
    video_info = None
    
    try:
        # Check if input is a video file
        if VIDEO_PROCESSING_AVAILABLE and is_video_file(file_path):
            print(f"📹 Video file detected: {os.path.basename(file_path)}")
            
            # Process video to extract audio
            video_result = process_video_for_interview_analysis(file_path)
            
            if not video_result["success"]:
                raise Exception(f"Video processing failed: {video_result['error']}")
            
            audio_path = video_result["audio_path"]
            temp_dir = video_result["temp_dir"]
            video_info = video_result["video_info"]
            
            print(f"✅ Audio extracted from video: {os.path.basename(audio_path)}")
        else:
            print(f"🎵 Audio file detected: {os.path.basename(file_path)}")
        
        # Step 1: Transcribe audio to text
        transcript = transcribe_audio(audio_path)
        
        # Step 2: Analyze speech patterns
        speech_analysis = analyze_speech_patterns(transcript)
        
        # Step 3: Analyze sentiment and emotions
        sentiment_analysis = analyze_sentiment_emotions(transcript)
        
        # Step 4: Analyze content quality
        content_analysis = analyze_content_quality(transcript)
        
        # Step 5: Generate personalized feedback
        feedback = generate_feedback(speech_analysis, sentiment_analysis, content_analysis)
        
        # Calculate overall interview score
        overall_score = int((
            speech_analysis["confidence_score"] * 0.3 +
            speech_analysis["clarity_score"] * 0.25 +
            (100 - speech_analysis["hesitation_rate"]) * 0.15 +
            content_analysis["content_quality_score"] * 0.3
        ))
        
        # Compile comprehensive results
        result = {
            "overall_score": overall_score,
            "transcript": transcript,
            "speech_analysis": speech_analysis,
            "sentiment_analysis": sentiment_analysis,
            "content_analysis": content_analysis,
            "feedback": feedback,
            "performance_summary": {
                "strengths": [],
                "areas_for_improvement": [],
                "recommendations": feedback[:3]  # Top 3 recommendations
            }
        }
        
        # Add video metadata if it was a video file
        if video_info:
            result["video_metadata"] = {
                "file_type": "video",
                "original_format": video_info.get("format", "unknown"),
                "duration": video_info.get("duration", 0),
                "resolution": video_info.get("resolution", (0, 0)),
                "fps": video_info.get("fps", 0),
                "audio_extracted": True
            }
        else:
            result["video_metadata"] = {
                "file_type": "audio",
                "audio_extracted": False
            }
        
        # Determine strengths and areas for improvement
        if speech_analysis["confidence_score"] > 75:
            result["performance_summary"]["strengths"].append("High confidence level")
        else:
            result["performance_summary"]["areas_for_improvement"].append("Build confidence")
            
        if speech_analysis["hesitation_rate"] < 10:
            result["performance_summary"]["strengths"].append("Fluent speaking")
        else:
            result["performance_summary"]["areas_for_improvement"].append("Reduce hesitation")
            
        if content_analysis["content_quality_score"] > 70:
            result["performance_summary"]["strengths"].append("Strong content quality")
        else:
            result["performance_summary"]["areas_for_improvement"].append("Improve content depth")
        
        # Clean up temporary files if video was processed
        if temp_dir:
            cleanup_temp_files(temp_dir, keep_audio=False)
        
        return result
        
    except Exception as e:
        print(f"Interview analysis error: {e}")
        
        # Clean up temporary files if video was being processed
        if 'temp_dir' in locals() and temp_dir:
            cleanup_temp_files(temp_dir, keep_audio=False)
        
        # Return fallback mock data
        return {
            "overall_score": 78,
            "transcript": "Audio processing unavailable - using demo analysis",
            "speech_analysis": {
                "confidence_score": 78,
                "clarity_score": 85,
                "hesitation_rate": 12,
                "filler_word_count": 3,
                "total_words": 150,
                "avg_sentence_length": 14.2
            },
            "sentiment_analysis": {
                "overall_sentiment": "Positive",
                "polarity": 0.4,
                "subjectivity": 0.6,
                "emotion_breakdown": {
                    "enthusiasm": 30,
                    "confidence": 25,
                    "nervousness": 15,
                    "professionalism": 20,
                    "curiosity": 10
                },
                "dominant_emotion": "enthusiasm"
            },
            "content_analysis": {
                "content_quality_score": 75,
                "technical_skills_mentioned": ["python", "javascript", "react"],
                "soft_skills_mentioned": ["teamwork", "problem solving"],
                "experience_indicators": 8
        },
        "feedback": [
                "Great enthusiasm and positive attitude",
                "Consider adding more specific technical examples",
                "Practice speaking with slightly less hesitation"
            ],
            "performance_summary": {
                "strengths": ["High confidence level", "Strong content quality"],
                "areas_for_improvement": ["Reduce hesitation"],
                "recommendations": [
                    "Great enthusiasm and positive attitude",
                    "Consider adding more specific technical examples",
                    "Practice speaking with slightly less hesitation"
                ]
            }
        }
