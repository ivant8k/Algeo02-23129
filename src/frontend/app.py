from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os
import json
from backend.image.imgtools import process_image_query, load_mapper

app = Flask(__name__)

# Folder penyimpanan file upload
UPLOAD_FOLDER = './test/uploads/'
DATASET_FOLDER = './test/dataset/'
QUERY_FOLDER = './test/query/'
MAPPER_PATH = './test/mapper.json'
IMAGE_SIZE = (64, 64)
K = 20

# Pastikan folder upload ada
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load mapper (global variable)
mapper = {}

@app.route('/')
def home():
    return render_template("index.html")  # Halaman utama

@app.route('/upload-dataset', methods=['POST'])
def upload_dataset():
    """
    Endpoint untuk mengunggah dataset gambar.
    """
    files = request.files.getlist('files[]')
    for file in files:
        filename = secure_filename(file.filename)
        file.save(os.path.join(DATASET_FOLDER, filename))
    return jsonify({"message": f"{len(files)} files uploaded successfully to dataset folder."})

@app.route('/upload-mapper', methods=['POST'])
def upload_mapper():
    """
    Endpoint untuk mengunggah mapper (JSON atau TXT).
    """
    global mapper
    file = request.files['mapper']
    filepath = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
    file.save(filepath)

    # Load mapper
    mapper = load_mapper(filepath)
    return jsonify({"message": "Mapper loaded successfully.", "mapper_keys": list(mapper.keys())})

@app.route('/query-image', methods=['POST'])
def query_image():
    """
    Endpoint untuk melakukan pencarian gambar dengan PCA.
    """
    file = request.files['query_image']
    query_path = os.path.join(QUERY_FOLDER, secure_filename(file.filename))
    file.save(query_path)

    # Jalankan proses pencarian
    result, execution_time = process_image_query(query_path, DATASET_FOLDER, IMAGE_SIZE, K, mapper)

    return jsonify({
        "query_image": file.filename,
        "results": result,
        "execution_time_ms": execution_time
    })

@app.route('/query-audio', methods=['POST'])
def query_audio():
    """
    Endpoint untuk melakukan pencarian audio.
    """
    # Implementasi query audio sesuai backend/audio
    pass  # Sesuaikan dengan fungsi audio retrieval

if __name__ == '__main__':
    app.run(debug=True)
