#!/usr/bin/env python3
"""
SkillSync AI Quick Fix

This script automatically fixes common Gemini AI issues.
"""

import os
from dotenv import load_dotenv

load_dotenv()

def auto_fix_gemini():
    """Automatically detect and fix Gemini model issues"""
    print("🔧 SkillSync AI Quick Fix")
    print("=" * 40)
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ No API key found")
        print("Please add GEMINI_API_KEY to your .env file")
        return False
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        
        print("🔍 Finding working model...")
        
        # Modern model names first
        model_candidates = [
            'gemini-1.5-flash-latest',
            'gemini-1.5-flash', 
            'gemini-1.5-pro-latest',
            'gemini-1.5-pro',
            'gemini-pro-latest',
            'gemini-pro'
        ]
        
        working_model = None
        
        for model_name in model_candidates:
            try:
                print(f"  Testing {model_name}...")
                model = genai.GenerativeModel(model_name)
                
                # Quick test
                response = model.generate_content("Say 'OK' if you're working")
                if response and response.text:
                    print(f"  ✅ {model_name} works!")
                    working_model = model_name
                    break
                    
            except Exception as e:
                print(f"  ❌ {model_name}: {str(e)[:50]}...")
                continue
        
        if working_model:
            print(f"\n🎉 Found working model: {working_model}")
            
            # Update ai_utils.py with the working model
            update_ai_utils(working_model)
            return True
        else:
            print("\n❌ No working models found")
            print("Try updating google-generativeai:")
            print("pip install --upgrade google-generativeai")
            return False
            
    except ImportError:
        print("❌ google-generativeai not installed")
        print("Install with: pip install google-generativeai")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def update_ai_utils(working_model):
    """Update ai_utils.py with the working model"""
    try:
        ai_utils_path = 'ai_utils.py'
        
        if not os.path.exists(ai_utils_path):
            print(f"⚠️  {ai_utils_path} not found in current directory")
            return
        
        with open(ai_utils_path, 'r') as f:
            content = f.read()
        
        # Simple replacement of the model initialization
        updated_content = content.replace(
            "model = genai.GenerativeModel(model_name)",
            f"model = genai.GenerativeModel('{working_model}')"
        )
        
        with open(ai_utils_path, 'w') as f:
            f.write(updated_content)
        
        print(f"✅ Updated ai_utils.py to use {working_model}")
        
    except Exception as e:
        print(f"⚠️  Could not update ai_utils.py: {e}")

def main():
    """Run the auto-fix"""
    success = auto_fix_gemini()
    
    print("\n" + "=" * 40)
    if success:
        print("🎉 AI fix complete!")
        print("\nNext steps:")
        print("1. Restart your backend: python app.py") 
        print("2. Test the AI features")
    else:
        print("❌ Auto-fix failed")
        print("\nManual steps:")
        print("1. Check your API key")
        print("2. Update packages: pip install --upgrade google-generativeai")
        print("3. Run diagnostics: python diagnose_ai.py")

if __name__ == "__main__":
    main() 