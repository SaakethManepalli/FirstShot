from flask import Flask, request, jsonify
from flask_cors import CORS
import os

#https://teenhacks.onrender.com/

import psycopg2
conn = psycopg2.connect(
    host="localhost",
    database="firstshot",
    user="saaketh",
    password="timmy",
    port="5432"
)

global sessionID
app = Flask(__name__)
CORS(app)

def update(sessionID, x, y):
    cur = conn.cursor()
    query = f'CREATE TABLE {sessionID} {x} INTEGER, {y} INTEGER'
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
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)