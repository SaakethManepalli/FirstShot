from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sqlite3
from datetime import datetime




def getTime():
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return current_time


#https://teenhacks.onrender.com/

conn = sqlite3.connect('firstshot.db', check_same_thread=False)

# Create a cursor object
cur = conn.cursor()

app = Flask(__name__)
CORS(app)

def update( x, y):
    query = (f'CREATE TABLE {getTime()} ('
             f' id INTEGER PRIMARY KEY AUTOINCREMENT,'
             f'{x} INTEGER,'
             f' {y} INTEGER')
    cur.execute(query)
    conn.commit()

@app.route('/')
def home():
    return jsonify({'message': 'Server is running'}), 200
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part in the request'}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        file_path = os.path.join('uploads', file.filename)
        os.makedirs('uploads', exist_ok=True)
        file.save(file_path)
        return jsonify({'message': 'Image uploaded successfully', 'file_path': file_path}), 200

@app.route('/sendback', methods=['POST'])
def send_back():
    data = request.get_json()
    print(data)
    update(data['sessionID'], data['x'], data['y'])
    return jsonify(data), 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5999))
    app.run(host='0.0.0.0', port=port, debug=True)