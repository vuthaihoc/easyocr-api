from flask import Flask, request, jsonify
import easyocr
import numpy as np
from PIL import Image
import io
import os
import json

app = Flask(__name__)

# Read GPU usage option from environment variable
USE_GPU = os.getenv('USE_GPU', 'False').lower() in ('true', '1', 't')

# Initialize EasyOCR reader
reader = easyocr.Reader(['en', 'vi'], gpu=USE_GPU)  # Use GPU if specified in environment variable


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

    # Lấy các tham số từ query
    paragraph = request.args.get('paragraph', 'False').lower() == 'true'
    output_format = request.args.get('output_format', 'json')
    decoder = request.args.get('decoder', 'greedy')
    merge_texts = request.args.get('merge_texts', 'False').lower() == 'true'

    if file:
        # Read the image file directly into memory
        image_bytes = file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        image_np = np.array(image)

        # Perform OCR
        json_result = reader.readtext(
            image_np,
            decoder=decoder,
            paragraph=paragraph,
            output_format=output_format,
        )

        if merge_texts is False:
            return json_result

        texts = extract_texts(json_result)

        return "\n".join(texts)

    return jsonify({"error": "File upload failed"}), 500


def extract_texts(json_array):
    texts = []
    for item in json_array:
        # Phân tích cú pháp chuỗi JSON
        parsed_item = json.loads(item)
        # Lấy trường 'text' và thêm vào danh sách
        texts.append(parsed_item['text'])
    return texts


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
