from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB limit
ALLOWED_EXTENSIONS = {'obj'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api', methods=['POST'])
def receive_file():
    try:
        # Check if the request has data
        if 'file' not in request.files:
            print("No file part in request")
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        
        # Check if a file was selected
        if file.filename == '':
            print("No selected file")
            return jsonify({"error": "No selected file"}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            print(f"File saved successfully at {file_path}")
            return jsonify({
                "message": "File received successfully",
                "filename": filename,
                "size": os.path.getsize(file_path)
            }), 200
        else:
            return jsonify({"error": "Invalid file type"}), 400
            
    except Exception as e:
        print(f"Error receiving file: {str(e)}")
        return jsonify({"error": f"Failed to process the file: {str(e)}"}), 500

# Handle file too large error
@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({"error": "File too large"}), 413

if __name__ == '__main__':
    app.run(debug=True)