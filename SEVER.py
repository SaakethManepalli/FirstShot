from flask import Flask, request, jsonify
from flask_cors import CORS
from pyngrok import ngrok, conf
import os
import ssl
import certifi

# Configure pyngrok to use the certifi certificate bundle
conf.get_default().cert_path = certifi.where()

app = Flask(__name__)
CORS(app)


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
    # Create uploads directory if it doesn't exist
    if not os.path.exists('uploads'):
        os.makedirs('uploads')

    try:
        # Configure SSL context
        ssl_context = ssl.create_default_context(cafile=certifi.where())

        # Start ngrok
        public_url = ngrok.connect(5000)
        print(f' * ngrok tunnel "http://127.0.0.1:5000" -> "{public_url}"')

        # Run Flask app
        app.run(port=5000, debug=True)
    except Exception as e:
        print(f"Error: {str(e)}")