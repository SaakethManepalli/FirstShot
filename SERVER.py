from flask import Flask, request, jsonify
from datetime import datetime
import os
import sqlite3
from flask_cors import CORS
import subprocess
import time
import json
#from SSPreProcessing import pre_process_ss

app = Flask(__name__)
CORS(app)

DATABASE = 'firstshot.db'

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_db():
    db = sqlite3.connect(DATABASE, detect_types=sqlite3.PARSE_DECLTYPES)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    db = get_db()
    try:
        cursor = db.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS session_data (id INTEGER PRIMARY KEY AUTOINCREMENT, session_id TEXT NOT NULL, x INTEGER NOT NULL, y INTEGER NOT NULL, timestamp TEXT NOT NULL);''')
        db.commit()
    finally:
        db.close()

def update_data(session_id, x, y):
    db = get_db()
    try:
        cursor = db.cursor()
        cursor.execute('''INSERT INTO session_data (session_id, x, y, timestamp) VALUES (?, ?, ?, ?);''', (session_id, x, y, get_timestamp()))
        db.commit()
    finally:
        db.close()

@app.route('/')
def home():
    return jsonify({'message': 'Server is running'}), 200

@app.route('/upload', methods=['POST'])
def upload_image():
    print(f"Received upload request: {request.content_type}")
    print(f"Files in request: {request.files.keys()}")

    if 'image' not in request.files:
        print("Error: No image part in the request")
        return jsonify({'error': 'No image part in the request'}), 400

    file = request.files['image']
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    if not file.filename or '.' not in file.filename or \
            file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
        print(f"Error: Invalid file type - {file.filename}")
        return jsonify({'error': 'Invalid file type'}), 400

    try:
        from werkzeug.utils import secure_filename
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_")
        filename = timestamp + filename
        file_path = os.path.join('uploads', filename)
        os.makedirs('uploads', exist_ok=True)
        file.save(file_path)

        print(f"Image saved successfully to {file_path}, filename: {filename}")
        response = jsonify({
            'message': 'Image uploaded successfully',
            'file_path': file_path,
            'filename': filename
        })

        #pre_process_ss(filename)

        response.status_code = 200

    except Exception as e:
        print(f"Error during file upload: {str(e)}")
        response = jsonify({'error': str(e)})
        response.status_code = 500

    return response

@app.route('/sendback', methods=['POST'])
def send_back():
    try:
        data = request.get_json()
        if not all(k in data for k in ['sessionID', 'x', 'y']):
            return jsonify({'error': 'Missing required fields'}), 400

        print(f"Inserting data into database: sessionID={data['sessionID']}, x={data['x']}, y={data['y']}")
        update_data(data['sessionID'], data['x'], data['y'])
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/getdata', methods=['GET'])
def getback():
    """Fetches session data from the database."""
    try:
        db = get_db()
        cursor = db.cursor()

        # Fetch everything, limit to 100 rows for performance
        cursor.execute('SELECT * FROM session_data LIMIT 100;')
        data = cursor.fetchall()

        if not data:
            return jsonify({'error': 'No data found'}), 404  # Explicit empty response

        # Convert rows to a list of dictionaries
        result = [dict(row) for row in data]
        app.logger.info(f"Data fetched successfully: {result}")
        return jsonify(result), 200
    except sqlite3.DatabaseError as db_error:
        error_message = {'error': f'Database error: {str(db_error)}'}
        app.logger.error(f"Database error: {error_message}")
        return jsonify(error_message), 500
    except Exception as e:
        error_message = {'error': f"Unexpected server error: {str(e)}"}
        app.logger.error(f"Server error: {error_message}")
        return jsonify(error_message), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'db' in locals():
            db.close()
if __name__ == '__main__':
    init_db()

    # Start Ngrok in a separate process
    ngrok_process = subprocess.Popen(['ngrok', 'http', '5999', '--domain=closing-blatantly-wahoo.ngrok-free.app'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Wait for Ngrok to start and get the public URL
    time.sleep(5)
    try:
        output = subprocess.check_output(['curl', '--silent', '--show-error', 'http://localhost:4040/api/tunnels'])
        tunnels = json.loads(output)
        public_url = tunnels['tunnels'][0]['public_url']
        print(f"Access your Flask app at: {public_url}")
    except Exception as e:
        print(f"Error retrieving Ngrok URL: {str(e)}")

    # Run Flask app
    port = int(os.environ.get('PORT', 5999))
    app.run(host='0.0.0.0', port=port)