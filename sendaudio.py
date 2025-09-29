import requests
import sys
import os
import logging
from logging.handlers import RotatingFileHandler
import time
import uuid

# Set up logging
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "audio_sender.log")

# Configure logger
logger = logging.getLogger("audio_sender")
logger.setLevel(logging.DEBUG)

# Clear any existing handlers
if logger.handlers:
    logger.handlers.clear()

# File handler with rotation (10MB max, keep 5 backups)
file_handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5, encoding="utf-8")
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(file_handler)

# Also add console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(console_handler)

def send_audio(audio_file_path, api_url):
    """
    Send an audio file to the backend without waiting for a response.
    """
    request_id = str(uuid.uuid4())[:8]  # Generate a short request ID for tracking
    logger.info(f"[{request_id}] Starting fire-and-forget audio upload: {audio_file_path} → {api_url}")
    
    if not os.path.exists(audio_file_path):
        logger.error(f"[{request_id}] File not found: {audio_file_path}")
        return False
    
    # Get file size for logging
    file_size = os.path.getsize(audio_file_path)
    logger.info(f"[{request_id}] File size: {file_size/1024:.2f} KB")
    
    start_time = time.time()
    
    try:
        # Prepare the file for upload
        with open(audio_file_path, 'rb') as audio_file:
            files = {
                'audio_file': audio_file  # Field name expected by Django view
            }
            
            logger.debug(f"[{request_id}] Sending POST request to {api_url}")
            
            # Use a very short timeout to achieve fire-and-forget behavior
            # The connection will be established but we won't wait for the response
            requests.post(
                api_url,
                files=files,
                timeout=0.5  # Very short timeout - just enough to establish connection
            )
            
    except requests.exceptions.Timeout:
        # This is expected and actually desired for fire-and-forget
        elapsed = time.time() - start_time
        logger.info(f"[{request_id}] Request sent successfully (timeout as expected): {elapsed:.2f}s")
        return True
    except requests.exceptions.RequestException as e:
        # This is an actual error (connection failed)
        logger.error(f"[{request_id}] Connection error: {e}")
        return False
    except Exception as e:
        logger.exception(f"[{request_id}] Unexpected error: {e}")
        return False
        
    # If we get here, the request completed faster than our timeout
    elapsed = time.time() - start_time
    logger.info(f"[{request_id}] Request completed before timeout: {elapsed:.2f}s")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sendaudio.py <audio_file_path> [api_url]")
        sys.exit(1)
        
    audio_file_path = sys.argv[1]
    api_url = sys.argv[2] if len(sys.argv) > 2 else "http://localhost:8080/transcribe/file" #"http://localhost:8001/api/stt/transcribe/"
    
    logger.info(f"Starting audio send process")
    success = send_audio(audio_file_path, api_url)
    
    if success:
        logger.info("Audio file send process completed")
    else:
        logger.error("Failed to send audio file")
        sys.exit(1)