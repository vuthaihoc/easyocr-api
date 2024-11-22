from flask import Flask, request, jsonify
import easyocr
import numpy as np
from PIL import Image
import io
import os

app = Flask(__name__)

# Read GPU usage option from environment variable
USE_GPU = os.getenv('USE_GPU', 'False').lower() in ('true', '1', 't')

# Initialize EasyOCR reader
reader = easyocr.Reader(['en','vi'], gpu=USE_GPU)  # Use GPU if specified in environment variable

@app.route('/health', methods=['GET'])
async def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/read', methods=['POST'])
async def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file:
        # Read the image file directly into memory
        image_bytes = file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        image_np = np.array(image)

        # Perform OCR
        json_result = reader.readtext(image_np, output_format = 'json')
        
        # Process result to return text
        #extracted_text = [text[1] for text in result]
        
        #return jsonify({"extracted_text": extracted_text})
        return json_result
    
    return jsonify({"error": "File upload failed"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
