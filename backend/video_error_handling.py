"""
Video Processing Error Handling

This module provides robust error handling for video processing operations.
It includes validation, recovery mechanisms, and user-friendly error messages.
"""

import os
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VideoProcessingError(Exception):
    """Custom exception for video processing errors"""
    pass

class VideoValidationError(VideoProcessingError):
    """Raised when video file validation fails"""
    pass

class AudioExtractionError(VideoProcessingError):
    """Raised when audio extraction fails"""
    pass

def validate_video_file(file_path, max_size_mb=100, max_duration_seconds=600):
    """
    Comprehensive video file validation
    
    Args:
        file_path (str): Path to the video file
        max_size_mb (int): Maximum file size in MB
        max_duration_seconds (int): Maximum duration in seconds
        
    Returns:
        dict: Validation result with details
        
    Raises:
        VideoValidationError: If validation fails
    """
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            raise VideoValidationError(f"Video file not found: {file_path}")
        
        # Check file size
        file_size_bytes = os.path.getsize(file_path)
        file_size_mb = file_size_bytes / (1024 * 1024)
        
        if file_size_mb > max_size_mb:
            raise VideoValidationError(
                f"Video file too large: {file_size_mb:.1f}MB (max: {max_size_mb}MB)"
            )
        
        # Check file extension
        file_ext = Path(file_path).suffix.lower()
        supported_formats = ['.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv', '.wmv', '.m4v']
        
        if file_ext not in supported_formats:
            raise VideoValidationError(
                f"Unsupported video format: {file_ext}. "
                f"Supported formats: {', '.join(supported_formats)}"
            )
        
        # Try to get video info (requires video processing libraries)
        try:
            from video_utils import get_video_info, VIDEO_PROCESSING_AVAILABLE
            
            if not VIDEO_PROCESSING_AVAILABLE:
                logger.warning("Video processing libraries not available - basic validation only")
                return {
                    "valid": True,
                    "file_size_mb": file_size_mb,
                    "format": file_ext,
                    "warning": "Advanced validation skipped - video libraries not available"
                }
            
            video_info = get_video_info(file_path)
            
            if "error" in video_info:
                raise VideoValidationError(f"Video file corrupted or unreadable: {video_info['error']}")
            
            # Check duration
            duration = video_info.get("duration", 0)
            if duration > max_duration_seconds:
                raise VideoValidationError(
                    f"Video too long: {duration:.1f}s (max: {max_duration_seconds}s)"
                )
            
            if duration < 1:
                raise VideoValidationError("Video file appears to be empty or corrupted")
            
            # Check resolution (warn if too low)
            resolution = video_info.get("resolution", (0, 0))
            if resolution[0] < 240 or resolution[1] < 240:
                logger.warning(f"Low video resolution: {resolution[0]}x{resolution[1]}")
            
            return {
                "valid": True,
                "file_size_mb": file_size_mb,
                "duration": duration,
                "resolution": resolution,
                "format": file_ext,
                "fps": video_info.get("fps", 0)
            }
            
        except ImportError:
            # Fallback to basic validation
            return {
                "valid": True,
                "file_size_mb": file_size_mb,
                "format": file_ext,
                "warning": "Advanced validation skipped - video libraries not available"
            }
        
    except VideoValidationError:
        raise
    except Exception as e:
        raise VideoValidationError(f"Validation failed: {str(e)}")

def safe_video_processing(file_path, max_retries=2):
    """
    Process video with error handling and retry logic
    
    Args:
        file_path (str): Path to the video file
        max_retries (int): Maximum number of retry attempts
        
    Returns:
        dict: Processing result
    """
    try:
        # First, validate the video file
        validation_result = validate_video_file(file_path)
        logger.info(f"Video validation passed: {validation_result}")
        
        # Import video processing utilities
        from video_utils import process_video_for_interview_analysis
        
        # Attempt video processing with retries
        last_error = None
        
        for attempt in range(max_retries + 1):
            try:
                logger.info(f"Video processing attempt {attempt + 1}/{max_retries + 1}")
                
                result = process_video_for_interview_analysis(file_path)
                
                if result["success"]:
                    logger.info("Video processing successful")
                    return {
                        "success": True,
                        "result": result,
                        "validation": validation_result,
                        "attempts": attempt + 1
                    }
                else:
                    last_error = result.get("error", "Unknown processing error")
                    logger.warning(f"Processing attempt {attempt + 1} failed: {last_error}")
                    
            except Exception as e:
                last_error = str(e)
                logger.warning(f"Processing attempt {attempt + 1} crashed: {last_error}")
                
                # If this is not the last attempt, wait briefly before retry
                if attempt < max_retries:
                    import time
                    time.sleep(1)
        
        # All attempts failed
        raise AudioExtractionError(f"Video processing failed after {max_retries + 1} attempts: {last_error}")
        
    except VideoValidationError as e:
        return {
            "success": False,
            "error": f"Validation failed: {str(e)}",
            "error_type": "validation",
            "user_message": str(e)
        }
    except AudioExtractionError as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": "processing",
            "user_message": "Failed to extract audio from video. Please try a different video file."
        }
    except Exception as e:
        logger.error(f"Unexpected error in video processing: {e}")
        return {
            "success": False,
            "error": str(e),
            "error_type": "unexpected",
            "user_message": "An unexpected error occurred during video processing."
        }

def get_user_friendly_error(error_type, error_message):
    """
    Convert technical errors to user-friendly messages
    
    Args:
        error_type (str): Type of error
        error_message (str): Technical error message
        
    Returns:
        dict: User-friendly error information
    """
    error_messages = {
        "validation": {
            "title": "Video File Issue",
            "suggestions": [
                "Check that your video file is not corrupted",
                "Ensure the file is in a supported format (MP4, AVI, MOV, etc.)",
                "Try reducing the file size if it's too large",
                "Make sure the video is not too long (max 10 minutes)"
            ]
        },
        "processing": {
            "title": "Processing Error",
            "suggestions": [
                "Try a different video file",
                "Ensure the video has a clear audio track",
                "Check that the video is not password protected",
                "Try converting the video to MP4 format"
            ]
        },
        "libraries": {
            "title": "System Configuration Issue",
            "suggestions": [
                "Video processing libraries need to be installed",
                "Contact your system administrator",
                "Try uploading an audio file instead (.mp3, .wav)"
            ]
        },
        "unexpected": {
            "title": "Unexpected Error",
            "suggestions": [
                "Try uploading your file again",
                "Check your internet connection",
                "Try a different video file",
                "Contact support if the problem persists"
            ]
        }
    }
    
    error_info = error_messages.get(error_type, error_messages["unexpected"])
    
    return {
        "title": error_info["title"],
        "message": error_message,
        "suggestions": error_info["suggestions"],
        "error_type": error_type
    }

def log_video_processing_stats(file_path, processing_time, success, error=None):
    """Log video processing statistics for monitoring"""
    stats = {
        "file_path": os.path.basename(file_path),
        "processing_time": processing_time,
        "success": success,
        "error": error
    }
    
    if success:
        logger.info(f"Video processing stats: {stats}")
    else:
        logger.error(f"Video processing failed: {stats}")
    
    # In a production system, you might send these stats to a monitoring service
    return stats 