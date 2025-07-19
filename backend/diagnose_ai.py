#!/usr/bin/env python3
"""
SkillSync AI Diagnostics

This script helps diagnose issues with Gemini AI setup.
Run this to check your API key and available models.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_environment():
    """Check environment setup"""
    print("🔍 SkillSync AI Diagnostics")
    print("=" * 50)
    
    # Check Python version
    print(f"Python version: {sys.version}")
    
    # Check environment variables
    api_key = os.getenv('GEMINI_API_KEY')
    if api_key:
        print(f"✅ GEMINI_API_KEY found (length: {len(api_key)})")
        # Don't print the full key for security
        print(f"   Starts with: {api_key[:10]}...")
    else:
        print("❌ GEMINI_API_KEY not found")
        return False
    
    return True

def check_dependencies():
    """Check if required packages are installed"""
    print("\n📦 Checking Dependencies")
    print("-" * 30)
    
    required_packages = [
        'google.generativeai',
        'python_dotenv',
        'flask',
        'flask_cors'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - NOT INSTALLED")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Install with: pip install " + ' '.join(missing_packages))
        return False
    
    return True

def test_gemini_api():
    """Test Gemini API connection and list available models"""
    print("\n🤖 Testing Gemini AI API")
    print("-" * 30)
    
    try:
        import google.generativeai as genai
        
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("❌ No API key found")
            return False
        
        # Configure API
        genai.configure(api_key=api_key)
        print("✅ API configured successfully")
        
        # List available models
        print("\n📋 Available Models:")
        try:
            models = genai.list_models()
            for model in models:
                if 'generateContent' in model.supported_generation_methods:
                    print(f"   ✅ {model.name}")
                else:
                    print(f"   ❌ {model.name} (doesn't support generateContent)")
        except Exception as e:
            print(f"   ⚠️  Could not list models: {e}")
        
        # Test model names
        model_names_to_test = [
            'gemini-1.5-flash',
            'gemini-1.5-pro',
            'gemini-pro',
            'models/gemini-1.5-flash',
            'models/gemini-1.5-pro',
            'models/gemini-pro'
        ]
        
        print("\n🧪 Testing Model Access:")
        working_model = None
        
        for model_name in model_names_to_test:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content("Hello, respond with 'OK'")
                print(f"   ✅ {model_name}: {response.text.strip()}")
                if not working_model:
                    working_model = model_name
            except Exception as e:
                print(f"   ❌ {model_name}: {e}")
        
        if working_model:
            print(f"\n🎉 Recommended model: {working_model}")
            return True
        else:
            print("\n❌ No working models found")
            return False
            
    except ImportError:
        print("❌ google-generativeai package not installed")
        print("Install with: pip install google-generativeai")
        return False
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

def test_skillsync_integration():
    """Test SkillSync AI integration"""
    print("\n🔧 Testing SkillSync Integration")
    print("-" * 30)
    
    try:
        from ai_utils import AI_ENABLED, generate_ai_resume_feedback
        
        if AI_ENABLED:
            print("✅ SkillSync AI is enabled")
            
            # Test with sample data
            sample_resume_data = {
                'similarity_score': 75,
                'matched_skills': ['Python', 'JavaScript'],
                'missing_skills': ['React', 'Docker'],
                'skill_categories': {
                    'Technical': ['Python', 'JavaScript'],
                    'Soft Skills': ['Communication']
                }
            }
            
            sample_job_description = "We need a developer with Python, JavaScript, React, and Docker experience."
            
            print("🧪 Testing AI feedback generation...")
            feedback = generate_ai_resume_feedback(sample_resume_data, sample_job_description)
            
            if feedback.get('ai_powered'):
                print("✅ AI feedback generation successful!")
                print(f"   Generated {len(feedback)} feedback sections")
            else:
                print("⚠️  Fell back to demo mode")
                
        else:
            print("❌ SkillSync AI is disabled")
            return False
            
    except Exception as e:
        print(f"❌ SkillSync integration test failed: {e}")
        return False
    
    return True

def main():
    """Run all diagnostic tests"""
    success = True
    
    success &= check_environment()
    success &= check_dependencies()
    success &= test_gemini_api()
    success &= test_skillsync_integration()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests passed! SkillSync AI should work properly.")
        print("\nNext steps:")
        print("1. Start the backend: python app.py")
        print("2. Open the frontend and test the AI features")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        print("\nCommon solutions:")
        print("1. Get API key: https://makersuite.google.com/app/apikey")
        print("2. Create .env file with: GEMINI_API_KEY=your_key_here")
        print("3. Install dependencies: pip install -r requirements.txt")
    
    print("\n💡 For more help, check the SETUP_INSTRUCTIONS.md file")

if __name__ == "__main__":
    main() 