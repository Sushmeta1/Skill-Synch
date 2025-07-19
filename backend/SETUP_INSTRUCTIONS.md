# 🚀 SkillSync AI Setup Instructions

## Quick Start (Demo Mode)

**Want to try SkillSync immediately?** It works perfectly without any API keys!

```bash
# Install basic dependencies
pip install -r requirements-basic.txt

# Start the server
python app.py
```

SkillSync will run in **demo mode** with high-quality simulated AI responses.

---

## Full AI Setup (Recommended)

### Step 1: Install Dependencies

```bash
# Install all dependencies including AI libraries
pip install -r requirements.txt
```

### Step 2: Get Gemini API Key (Free)

1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key

### Step 3: Configure Environment

**Option A: Run the setup helper**
```bash
python config.py
```

**Option B: Manual setup**
```bash
# Create .env file in the backend folder
echo "GEMINI_API_KEY=your_actual_api_key_here" > .env
```

### Step 4: Start SkillSync

```bash
python app.py
```

You should see:
```
✅ Gemini AI initialized successfully!
✅ SkillSync backend running on http://127.0.0.1:5000
```

---

## Troubleshooting

### ❌ "ModuleNotFoundError: No module named 'speech_recognition'"

**Solution:**
```bash
pip install SpeechRecognition pydub textblob numpy
```

### ❌ "Gemini API key not found" or Model Errors

**Quick Fix:**
```bash
python diagnose_ai.py  # Check what's wrong
python fix_ai.py       # Auto-fix common issues
```

**Manual Fix:**
1. Get API key from https://makersuite.google.com/app/apikey
2. Create `.env` file: `GEMINI_API_KEY=your_key_here`
3. Update packages: `pip install --upgrade google-generativeai`

### ❌ "Error with speech recognition service"

The app falls back to demo transcripts. For real speech recognition, ensure:
- Internet connection is available
- Audio files are in supported formats (.mp3, .wav, .m4a)

### ❌ Dependencies installation fails

Try installing step by step:
```bash
pip install flask flask-cors python-docx PyPDF2 docx2txt
pip install google-generativeai python-dotenv
pip install SpeechRecognition pydub textblob  # Optional for audio
```

---

## Features by Mode

### 🟢 Demo Mode (No API Key)
- ✅ Full resume analysis
- ✅ Skill extraction and matching
- ✅ Course recommendations
- ✅ Interview analysis with demo transcripts
- ✅ High-quality simulated AI feedback
- ✅ All UI features work perfectly

### 🚀 AI Mode (With Gemini API Key)
- ✅ Everything in Demo Mode, PLUS:
- 🤖 **Real AI-powered feedback** from Gemini
- 🎯 **Personalized career coaching**
- 📊 **Industry-specific insights**
- 🎤 **Real speech-to-text** (if audio libs installed)
- 💡 **Dynamic recommendation engine**

---

## Environment Variables

Create a `.env` file in the `backend/` folder:

```env
# Required for full AI features
GEMINI_API_KEY=your_gemini_api_key_here

# Optional settings
ENVIRONMENT=development
DEBUG=true
```

---

## Testing Your Setup

1. **Start the backend:**
   ```bash
   cd backend
   python app.py
   ```

2. **Open frontend:**
   ```bash
   cd ../SkillSync
   # Open index.html in browser or:
   python -m http.server 8000
   ```

3. **Test features:**
   - Upload a sample resume
   - Try the demo job description
   - Check if AI feedback appears
   - Upload an audio file for interview analysis

---

## API Usage Limits

**Gemini API (Free Tier):**
- 60 requests per minute
- 1,500 requests per day
- Perfect for testing and demos!

**For production:** Consider upgrading to paid tier for higher limits.

---

## Need Help?

1. **Check the console** for error messages
2. **Run `python config.py`** for setup diagnostics
3. **Try demo mode first** to verify basic functionality
4. **Check the main README.md** for comprehensive documentation

**Remember:** SkillSync is designed to work beautifully with or without AI features! 🎉 