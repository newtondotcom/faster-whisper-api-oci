from flask import Flask, request, jsonify
from mutagen import File
from utils import format_duration
from fw_utils import transcribe
from auth import verify_api_key_from_env
from functools import wraps
from dotenv import load_dotenv
import os
import uuid

# Load environment variables
load_dotenv()

app = Flask(__name__)


def require_api_key(f):
    """
    Decorator to require API key authentication for a route.
    Expects 'Authorization: Bearer <api_key>' header.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check Authorization header
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return jsonify({"error": "Missing or invalid Authorization header. Use 'Bearer <api_key>'"}), 401
        
        api_key = auth_header.split(' ', 1)[1] if ' ' in auth_header else None
        
        if not api_key:
            return jsonify({"error": "API key not provided"}), 401
        
        # Verify API key
        if not verify_api_key_from_env(api_key):
            return jsonify({"error": "Invalid API key"}), 401
        
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/health")
def health():
    """
    Health check endpoint. Returns 200 if the service is running.
    """
    return jsonify({"status": "healthy"}), 200

@app.route("/duration", methods=["POST"])
@require_api_key
def transcription():
    """
    Accepts an MP3 or WAV file upload and returns its duration in seconds.
    """
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files["file"]
    
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400
    
    # Check file extension
    filename = file.filename.lower()
    if not (filename.endswith(".mp3") or filename.endswith(".wav")):
        return jsonify({"error": "File must be MP3 or WAV format"}), 400
    
    try:
        # Save uploaded file temporarily
        temp_path = f"/tmp/{file.filename}"
        file.save(temp_path)
        
        # Get audio duration using mutagen
        audio_file = File(temp_path)
        if audio_file is None:
            return jsonify({"error": "Could not read audio file"}), 400
        
        duration = audio_file.info.length
        
        # Clean up temporary file
        os.remove(temp_path)
        
        return jsonify({
            "filename": file.filename,
            "duration_seconds": round(duration, 2),
            "duration_formatted": format_duration(duration)
        }), 200
        
    except Exception as e:
        # Clean up temporary file if it exists
        temp_path = f"/tmp/{file.filename}"
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return jsonify({"error": str(e)}), 500

@app.route("/transcribe", methods=["POST"])
@require_api_key
def transcribe_route():
    """
    Accepts an MP3 or WAV file upload and returns its transcription.
    """
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files["file"]
    
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400
    
    # Check file extension
    filename = file.filename.lower()
    if not (filename.endswith(".mp3") or filename.endswith(".wav")):
        return jsonify({"error": "File must be MP3 or WAV format"}), 400
    
    # Generate unique temp file path to avoid collisions
    file_ext = os.path.splitext(file.filename)[1]
    temp_path = f"/tmp/{uuid.uuid4()}{file_ext}"
    
    try:
        # Save uploaded file temporarily
        file.save(temp_path)
        
        # Transcribe the audio file
        segments = transcribe(temp_path)
        
        # Format segments for JSON response
        formatted_segments = []
        full_text = ""
        for segment in segments:
            segment_data = {
                "start": round(segment.start, 2),
                "end": round(segment.end, 2),
                "text": segment.text.strip()
            }
            formatted_segments.append(segment_data)
            full_text += segment.text.strip() + " "
        
        # Clean up temporary file
        os.remove(temp_path)
        
        return jsonify({
            "filename": file.filename,
            "segments": formatted_segments,
            "text": full_text.strip()
        }), 200
        
    except Exception as e:
        # Clean up temporary file if it exists
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
	host = os.getenv('FLASK_HOST', '0.0.0.0')
	port = int(os.getenv('FLASK_PORT', '5000'))
	debug = os.getenv('FLASK_DEBUG', 'True').lower() in ('true', '1', 'yes')
	app.run(host=host, port=port, debug=debug)