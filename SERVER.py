from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sqlite3
from datetime import datetime

#teenhacks.onrender.com
app = Flask(__name__)
CORS(app)

DATABASE = 'firstshot.db'


def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# Initialize database connection with explicit SQL dialect specification
def get_db():
    db = sqlite3.connect(DATABASE, detect_types=sqlite3.PARSE_DECLTYPES)
    db.row_factory = sqlite3.Row
    return db


def init_db():
    db = get_db()
    try:
        cursor = db.cursor()
        # Using explicit SQLite syntax
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS session_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                x INTEGER NOT NULL,
                y INTEGER NOT NULL,
                timestamp TEXT NOT NULL
            );
        ''')
        db.commit()
    finally:
        db.close()


def update_data(session_id, x, y):
    db = get_db()
    try:
        cursor = db.cursor()
        # Using explicit SQLite INSERT syntax
        cursor.execute('''
            INSERT INTO session_data 
            (session_id, x, y, timestamp) 
            VALUES (?, ?, ?, ?);
        ''', (session_id, x, y, get_timestamp()))
        db.commit()
    finally:
        db.close()


@app.route('/')
def home():
    return jsonify({'message': 'Server is running'}), 200

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        print("Error: No image part in the request")
        return jsonify({'error': 'No image part in the request'}), 400

    file = request.files['image']
    if file.filename == '':
        print("Error: No selected file")
        return jsonify({'error': 'No selected file'}), 400

    try:
        file_path = os.path.join('uploads', file.filename)
        os.makedirs('uploads', exist_ok=True)
        file.save(file_path)
        return jsonify({
            'message': 'Image uploaded successfully',
            'file_path': file_path
        }), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/sendback', methods=['POST'])
def send_back():
    try:
        data = request.get_json()
        if not all(k in data for k in ['sessionID', 'x', 'y']):
            return jsonify({'error': 'Missing required fields'}), 400

        update_data(data['sessionID'], data['x'], data['y'])
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/getdata', methods=['GET'])
def getback():
    init_db()
    try:
        cursor = db.cursor()
        cursor.execute('SELECT * FROM session_data;')
        data = cursor.fetchall()
        return jsonify([dict(row) for row in data]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    init_db()  # Initialize database and tables
    port = int(os.environ.get('PORT', 5999))
    app.run(host='0.0.0.0', port=port, debug=True)