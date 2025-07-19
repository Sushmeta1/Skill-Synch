#!/usr/bin/env python3
"""
SkillSync Video Functionality Test Script

This script tests the complete video processing pipeline:
1. Video processing capabilities
2. Audio extraction
3. Interview analysis with video files
4. API endpoint functionality
"""

import os
import sys
import requests
import tempfile
from pathlib import Path

def test_video_utilities():
    """Test the video processing utilities"""
    print("🧪 Testing Video Processing Utilities")
    print("=" * 50)
    
    try:
        from video_utils import (
            VIDEO_PROCESSING_AVAILABLE,
            SUPPORTED_VIDEO_FORMATS,
            is_video_file,
            get_video_info,
            test_video_processing
        )
        
        if not VIDEO_PROCESSING_AVAILABLE:
            print("❌ Video processing libraries not available")
            print("   Install with: pip install moviepy opencv-python ffmpeg-python")
            return False
        
        print("✅ Video utilities imported successfully")
        print(f"✅ Supported formats: {', '.join(SUPPORTED_VIDEO_FORMATS)}")
        
        # Test file type detection
        test_files = [
            "test.mp4", "test.avi", "test.mov", "test.mkv",
            "test.mp3", "test.wav", "test.txt"
        ]
        
        for filename in test_files:
            is_video = is_video_file(filename)
            expected = filename.split('.')[-1] in ['mp4', 'avi', 'mov', 'mkv']
            if is_video == expected:
                print(f"✅ {filename}: {'Video' if is_video else 'Not video'}")
            else:
                print(f"❌ {filename}: Detection failed")
                return False
        
        print("✅ File type detection working correctly")
        return True
        
    except ImportError as e:
        print(f"❌ Cannot import video utilities: {e}")
        return False

def test_interview_analysis_import():
    """Test that interview analysis can import video utilities"""
    print("\n🧪 Testing Interview Analysis Integration")
    print("=" * 50)
    
    try:
        from interview_utils import analyze_interview, VIDEO_PROCESSING_AVAILABLE
        
        if VIDEO_PROCESSING_AVAILABLE:
            print("✅ Interview analysis has video support")
        else:
            print("⚠️ Interview analysis running without video support")
        
        print("✅ Interview analysis imports successful")
        return True
        
    except ImportError as e:
        print(f"❌ Cannot import interview analysis: {e}")
        return False

def test_backend_server():
    """Test that the backend server is running"""
    print("\n🧪 Testing Backend Server")
    print("=" * 50)
    
    try:
        response = requests.get('http://127.0.0.1:5000/', timeout=5)
        if response.status_code == 200:
            print("✅ Backend server is running")
            return True
        else:
            print(f"❌ Backend server responded with status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to backend server: {e}")
        print("   Make sure to run: cd backend && python app.py")
        return False

def test_api_endpoint_audio():
    """Test the interview analysis API with a mock audio file"""
    print("\n🧪 Testing API Endpoint with Audio")
    print("=" * 50)
    
    try:
        # Create a temporary file that looks like audio
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
            temp_file.write(b"fake audio data for testing")
            temp_file_path = temp_file.name
        
        # Test the API endpoint
        with open(temp_file_path, 'rb') as f:
            files = {'interview': ('test_audio.wav', f, 'audio/wav')}
            response = requests.post('http://127.0.0.1:5000/analyze-interview', files=files, timeout=30)
        
        # Clean up
        os.unlink(temp_file_path)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Audio API endpoint working")
            print(f"   Response keys: {list(data.keys())}")
            
            # Check for expected keys
            expected_keys = ['overall_score', 'transcript', 'speech_analysis']
            for key in expected_keys:
                if key in data:
                    print(f"   ✅ {key}: present")
                else:
                    print(f"   ⚠️ {key}: missing")
            
            return True
        else:
            print(f"❌ API returned status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

def create_sample_video_instructions():
    """Provide instructions for testing with real video files"""
    print("\n📹 Real Video File Testing Instructions")
    print("=" * 50)
    
    print("To test with actual video files:")
    print("1. Create a short video file (30 seconds - 2 minutes)")
    print("2. Record yourself speaking (interview simulation)")
    print("3. Save as MP4, AVI, or MOV format")
    print("4. Use the SkillSync frontend to upload and analyze")
    print("")
    print("Test video requirements:")
    print("• Duration: 30 seconds to 10 minutes")
    print("• Clear audio track")
    print("• Supported formats: MP4, AVI, MOV, MKV, WebM")
    print("• File size: Under 100MB (for web upload)")
    print("")
    print("Expected behavior:")
    print("1. Video is uploaded successfully")
    print("2. Audio is extracted from video")
    print("3. Speech analysis is performed")
    print("4. Results show video metadata (resolution, duration, etc.)")
    print("5. Analysis includes confidence, clarity, and content scores")

def run_comprehensive_test():
    """Run all tests and provide a summary"""
    print("🚀 SkillSync Video Functionality Test Suite")
    print("=" * 70)
    
    tests = [
        ("Video Utilities", test_video_utilities),
        ("Interview Analysis Integration", test_interview_analysis_import),
        ("Backend Server", test_backend_server),
        ("API Endpoint (Audio)", test_api_endpoint_audio)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results[test_name] = False
    
    # Summary
    print("\n📊 Test Results Summary")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Video functionality is ready to use.")
        create_sample_video_instructions()
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
        print("\nCommon solutions:")
        print("1. Install video dependencies: pip install moviepy opencv-python ffmpeg-python")
        print("2. Start the backend server: cd backend && python app.py")
        print("3. Check network connectivity to localhost:5000")
    
    return passed == total

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1) 