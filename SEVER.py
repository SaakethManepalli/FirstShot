from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import subprocess

app = Flask(__name__)
CORS(app)

@app.route('/')
def TEST():
    return "Hello, World!"
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part in the request'}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)
        return jsonify({'message': 'Image uploaded successfully', 'file_path': file_path}), 200


if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')

    # Install localtunnel if not already installed
    try:
        subprocess.run(['npx', 'localtunnel', '--version'], check=True)
    except:
        print("Installing localtunnel...")
        subprocess.run(['npm', 'install', '-g', 'localtunnel'])

    # Start localtunnel in a separate process
    tunnel_process = subprocess.Popen(['npx', 'localtunnel', '--port', '5000'],
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE,
                                      universal_newlines=True)

    print("Starting tunnel...")
    # Wait a moment for the tunnel to start and get the URL
    import time

    time.sleep(2)

    try:
        # Run Flask app
        print("Starting Flask server...")
        app.run(port=5000, debug=True)
    finally:
        tunnel_process.terminate()