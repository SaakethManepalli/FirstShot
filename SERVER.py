from flask import Flask, request, jsonify
from datetime import datetime
import os
import sqlite3
from flask_cors import CORS
import subprocess
import time
import json
import logging
from contextlib import contextmanager
from typing import Optional, Dict, List, Union
from werkzeug.utils import secure_filename
import random
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Configuration
DATABASE = 'firstshot.db'
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
DEFAULT_PORT = 5999
NGROK_DOMAIN = 'closing-blatantly-wahoo.ngrok-free.app'

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def get_timestamp() -> str:
    """Return current timestamp in consistent format."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@contextmanager
def get_db():
    """Context manager for database connections."""
    db = None
    try:
        db = sqlite3.connect(
            DATABASE,
            detect_types=sqlite3.PARSE_DECLTYPES,
            timeout=20
        )
        db.row_factory = sqlite3.Row
        yield db
    except sqlite3.Error as e:
        logger.error(f"Database connection error: {e}")
        raise
    finally:
        if db is not None:
            db.close()


def init_db() -> None:
    """Initialize the database with required tables."""
    try:
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS session_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    x INTEGER NOT NULL,
                    y INTEGER NOT NULL,
                    timestamp TEXT NOT NULL
                );
            ''')
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_session_id ON session_data(session_id);
            ''')
            db.commit()
            logger.info("Database initialized successfully")
    except sqlite3.Error as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed."""
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def validate_coordinates(x: Union[int, float], y: Union[int, float]) -> bool:
    """Validate coordinate values."""
    try:
        return isinstance(x, (int, float)) and isinstance(y, (int, float))
    except (TypeError, ValueError):
        return False


def update_data(session_id: str, x: Union[int, float], y: Union[int, float]) -> None:
    """
    Update session data in the database.

    Args:
        session_id: Unique identifier for the session
        x: X coordinate
        y: Y coordinate

    Raises:
        ValueError: If coordinates are invalid
        sqlite3.Error: If database operation fails
    """
    if not session_id or not isinstance(session_id, str):
        raise ValueError("Invalid session ID")

    if not validate_coordinates(x, y):
        raise ValueError("Invalid coordinates")

    try:
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute(
                '''INSERT INTO session_data (session_id, x, y, timestamp)
                   VALUES (?, ?, ?, ?);''',
                (session_id, x, y, get_timestamp())
            )
            db.commit()
            logger.info(f"Data updated for session {session_id}")
    except sqlite3.Error as e:
        logger.error(f"Failed to update data: {e}")
        raise


def get_session_data(limit: Optional[int] = 100) -> List[Dict]:
    """
    Retrieve session data from the database.

    Args:
        limit: Maximum number of records to retrieve

    Returns:
        List of dictionaries containing session data

    Raises:
        sqlite3.Error: If database operation fails
    """
    try:
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute(
                'SELECT * FROM session_data ORDER BY timestamp DESC LIMIT ?;',
                (limit,)
            )
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    except sqlite3.Error as e:
        logger.error(f"Failed to retrieve data: {e}")
        raise


# Route handlers
@app.route('/')
def home():
    """Health check endpoint."""
    return jsonify({'message': 'Server is running', 'timestamp': get_timestamp()}), 200


@app.route('/upload', methods=['POST'])
def upload_image():
    """Handle image upload."""
    logger.info(f"Received upload request: {request.content_type}")
    logger.debug(f"Files in request: {list(request.files.keys())}")

    if 'image' not in request.files:
        logger.warning("No image part in the request")
        return jsonify({'error': 'No image part in the request'}), 400

    file = request.files['image']

    if not file.filename:
        logger.warning("No selected file")
        return jsonify({'error': 'No selected file'}), 400

    if not allowed_file(file.filename):
        logger.warning(f"Invalid file type: {file.filename}")
        return jsonify({'error': 'Invalid file type'}), 400

    try:
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_")
        filename = timestamp + filename
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        file.save(file_path)
        logger.info(f"Image saved successfully: {file_path}")

        # Optional: Process the screenshot if needed
        # pre_process_ss(filename)

        return jsonify({
            'message': 'Image uploaded successfully',
            'file_path': file_path,
            'filename': filename
        }), 200

    except Exception as e:
        logger.error(f"Error during file upload: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/sendback', methods=['POST'])
def send_back():
    """Handle session data updates."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        if not all(k in data for k in ['sessionID', 'x', 'y']):
            return jsonify({'error': 'Missing required fields'}), 400

        update_data(data['sessionID'], data['x'], data['y'])
        return jsonify({
            'message': 'Data updated successfully',
            'data': data
        }), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except sqlite3.Error as e:
        return jsonify({'error': f"Database error: {str(e)}"}), 500
    except Exception as e:
        logger.error(f"Unexpected error in send_back: {e}")
        return jsonify({'error': "Internal server error"}), 500


@app.route('/getdata', methods=['GET'])
def getback():
    """Retrieve session data."""
    try:
        # Ensure the limit parameter is valid
        limit = request.args.get('limit', default=100, type=int)
        if limit < 1:
            return jsonify({'error': 'Invalid limit parameter'}), 400

        # Fetch session data from the database
        result = get_session_data(limit)
        if not result:
            # If no data is found, respond with empty data
            return jsonify({'message': 'No data found', 'data': []}), 200

        # If data is found, return it
        return jsonify({
            'message': 'Data retrieved successfully',
            'count': len(result),
            'data': result
        }), 200

    except sqlite3.Error as e:
        # Handle database errors gracefully
        logger.error(f"Database error: {str(e)}")
        return jsonify({'error': f"Database error: {str(e)}"}), 500

    except Exception as e:
        # Catch any unexpected exceptions and log them
        logger.error(f"Unexpected error in /getdata: {e}")
        return jsonify({'error': f"Unexpected server error: {str(e)}"}), 500



def start_ngrok() -> Optional[str]:
    """Start ngrok service and return public URL."""
    try:
        ngrok_process = subprocess.Popen(
            ['ngrok', 'http', str(DEFAULT_PORT), f'--domain={NGROK_DOMAIN}'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # Wait for ngrok to start
        time.sleep(5)

        # Get the public URL
        output = subprocess.check_output(
            ['curl', '--silent', '--show-error', 'http://localhost:4040/api/tunnels']
        )
        tunnels = json.loads(output)
        public_url = tunnels['tunnels'][0]['public_url']
        logger.info(f"Ngrok tunnel established at: {public_url}")
        return public_url

    except Exception as e:
        logger.error(f"Error starting ngrok: {str(e)}")
        return None

if __name__ == '__main__':
    # Initialize the database
    init_db()

    # Start ngrok
    public_url = start_ngrok()
    if public_url:
        print(f"Access your Flask app at: {public_url}")
    else:
        print("Warning: Failed to start ngrok tunnel")

    # Start Flask app
    port = int(os.environ.get('PORT', DEFAULT_PORT))
    app.run(host='0.0.0.0', port=port)