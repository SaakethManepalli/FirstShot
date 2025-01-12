from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import subprocess
import time

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Server is running'})

@app.route('/test', methods=['POST'])
def test():
    data = request.json
    return jsonify({
        'status': 'success',
        'received_data': data
    })

if __name__ == '__main__':
    # Start LocalTunnel in a separate process
    localtunnel_process = subprocess.Popen(['lt', '--port', '5000'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Wait for LocalTunnel to start and get the public URL
    time.sleep(2)
    output = localtunnel_process.stdout.readline().decode('utf-8').strip()
    print(f"Access your Flask app at: {output}")

    # Run Flask app
    app.run(port=5000, debug=True)