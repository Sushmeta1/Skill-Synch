import os
import tempfile
from pathlib import Path

# Try importing video processing libraries
try:
    from moviepy.editor import VideoFileClip
    import cv2
    import ffmpeg
    VIDEO_PROCESSING_AVAILABLE = True
    print("✅ Video processing libraries loaded successfully")
except ImportError as e:
    VIDEO_PROCESSING_AVAILABLE = False
    print(f"⚠️ Video processing libraries not available: {e}")
    print("   Install with: pip install moviepy opencv-python ffmpeg-python")

# Supported video formats
SUPPORTED_VIDEO_FORMATS = ['.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv', '.wmv', '.m4v']

def is_video_file(file_path):
    """Check if file is a supported video format"""
    file_extension = Path(file_path).suffix.lower()
    return file_extension in SUPPORTED_VIDEO_FORMATS

def get_video_info(video_path):
    """Get basic information about the video file"""
    if not VIDEO_PROCESSING_AVAILABLE:
        return {
            "duration": 0,
            "fps": 0,
            "resolution": (0, 0),
            "format": "unknown",
            "error": "Video processing libraries not available"
        }
    
    try:
        # Use OpenCV to get video information
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            return {"error": "Could not open video file"}
        
        # Get video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        duration = frame_count / fps if fps > 0 else 0
        
        cap.release()
        
        return {
            "duration": round(duration, 2),
            "fps": round(fps, 2),
            "resolution": (width, height),
            "frame_count": int(frame_count),
            "format": Path(video_path).suffix.lower()
        }
        
    except Exception as e:
        return {"error": f"Failed to get video info: {str(e)}"}

def extract_audio_from_video(video_path, output_audio_path=None):
    """
    Extract audio from video file and save as WAV for speech recognition
    
    Args:
        video_path (str): Path to the video file
        output_audio_path (str): Optional path for output audio file
        
    Returns:
        str: Path to the extracted audio file
    """
    if not VIDEO_PROCESSING_AVAILABLE:
        raise Exception("Video processing libraries not installed. Please install moviepy and ffmpeg-python.")
    
    try:
        # Generate output path if not provided
        if output_audio_path is None:
            video_name = Path(video_path).stem
            output_audio_path = f"{video_name}_extracted_audio.wav"
        
        # Use MoviePy to extract audio
        with VideoFileClip(video_path) as video_clip:
            # Extract audio
            audio_clip = video_clip.audio
            
            # Save as WAV file (best for speech recognition)
            audio_clip.write_audiofile(
                output_audio_path,
                codec='pcm_s16le',  # Uncompressed WAV
                fps=44100,          # Standard sample rate
                nbytes=2,           # 16-bit depth
                verbose=False,      # Suppress MoviePy output
                logger=None         # Suppress logging
            )
            
            audio_clip.close()
        
        print(f"✅ Audio extracted successfully: {output_audio_path}")
        return output_audio_path
        
    except Exception as e:
        print(f"❌ Failed to extract audio: {str(e)}")
        raise Exception(f"Audio extraction failed: {str(e)}")

def extract_audio_with_ffmpeg(video_path, output_audio_path=None):
    """
    Alternative audio extraction using ffmpeg directly (faster)
    """
    if not VIDEO_PROCESSING_AVAILABLE:
        raise Exception("FFmpeg not available")
    
    try:
        if output_audio_path is None:
            video_name = Path(video_path).stem
            output_audio_path = f"{video_name}_extracted_audio.wav"
        
        # Use ffmpeg for audio extraction
        stream = ffmpeg.input(video_path)
        audio = stream.audio
        out = ffmpeg.output(audio, output_audio_path, acodec='pcm_s16le', ac=1, ar='16000')
        ffmpeg.run(out, overwrite_output=True, quiet=True)
        
        print(f"✅ Audio extracted with FFmpeg: {output_audio_path}")
        return output_audio_path
        
    except Exception as e:
        print(f"❌ FFmpeg extraction failed: {str(e)}")
        # Fallback to MoviePy
        return extract_audio_from_video(video_path, output_audio_path)

def process_video_for_interview_analysis(video_path, temp_dir=None):
    """
    Complete video processing pipeline for interview analysis
    
    Args:
        video_path (str): Path to the uploaded video file
        temp_dir (str): Optional temporary directory for processing
        
    Returns:
        dict: Processing results with audio path and video metadata
    """
    try:
        # Create temporary directory if not provided
        if temp_dir is None:
            temp_dir = tempfile.mkdtemp()
        
        # Validate video file
        if not is_video_file(video_path):
            raise Exception(f"Unsupported video format. Supported formats: {', '.join(SUPPORTED_VIDEO_FORMATS)}")
        
        # Get video information
        video_info = get_video_info(video_path)
        if "error" in video_info:
            raise Exception(video_info["error"])
        
        # Check video duration (limit to reasonable length)
        max_duration = 600  # 10 minutes
        if video_info.get("duration", 0) > max_duration:
            raise Exception(f"Video too long. Maximum duration: {max_duration} seconds")
        
        # Extract audio
        audio_filename = f"extracted_audio_{os.path.basename(video_path)}.wav"
        audio_path = os.path.join(temp_dir, audio_filename)
        
        extracted_audio_path = extract_audio_from_video(video_path, audio_path)
        
        # Verify audio file was created
        if not os.path.exists(extracted_audio_path):
            raise Exception("Audio extraction completed but file not found")
        
        return {
            "success": True,
            "audio_path": extracted_audio_path,
            "video_info": video_info,
            "original_video": video_path,
            "temp_dir": temp_dir
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "video_info": video_info if 'video_info' in locals() else None
        }

def cleanup_temp_files(temp_dir, keep_audio=False):
    """Clean up temporary files after processing"""
    try:
        if temp_dir and os.path.exists(temp_dir):
            for file in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, file)
                if keep_audio and file.endswith('.wav'):
                    continue  # Keep audio file for analysis
                os.remove(file_path)
            
            if not keep_audio:
                os.rmdir(temp_dir)
                
        print("✅ Temporary files cleaned up")
    except Exception as e:
        print(f"⚠️ Cleanup warning: {e}")

# Demo/testing function
def test_video_processing():
    """Test video processing capabilities"""
    print("🧪 Testing Video Processing Capabilities")
    print("=" * 50)
    
    if not VIDEO_PROCESSING_AVAILABLE:
        print("❌ Video processing libraries not available")
        print("   Install with: pip install moviepy opencv-python ffmpeg-python")
        return False
    
    print("✅ All video processing libraries are available")
    print("✅ Supported video formats:", ', '.join(SUPPORTED_VIDEO_FORMATS))
    
    return True

if __name__ == "__main__":
    test_video_processing() 