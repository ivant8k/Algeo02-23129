from flask import Flask, request, jsonify, render_template
import os
from werkzeug.utils import secure_filename
# Import fungsi PCA
from imgtools import process_image_query, DATASET_FOLDER, QUERY_FOLDER, MAPPER_PATH

# Inisialisasi Flask app
app = Flask(__name__)

# Konfigurasi folder upload
os.makedirs(DATASET_FOLDER, exist_ok=True)
os.makedirs(QUERY_FOLDER, exist_ok=True)

# Halaman Utama
@app.route('/')
def home():
    return render_template("index.html")

# Upload Dataset
@app.route('/upload-dataset', methods=['POST'])
def upload_dataset():
    if 'file' not in request.files:
        return jsonify({"error": "Dataset tidak ditemukan!"}), 400
    
    file = request.files['file']
    filename = secure_filename(file.filename)
    filepath = os.path.join(DATASET_FOLDER, filename)
    file.save(filepath)
    
    return jsonify({"message": f"Dataset {filename} berhasil diunggah!", "path": filepath})

# Upload Mapper (Opsional)
@app.route('/upload-mapper', methods=['POST'])
def upload_mapper():
    if 'file' not in request.files:
        return jsonify({"error": "Mapper tidak ditemukan!"}), 400
    
    file = request.files['file']
    filepath = os.path.join(MAPPER_PATH)
    file.save(filepath)
    
    return jsonify({"message": "Mapper berhasil diunggah!", "path": filepath})

# Query Image (Album Finder with PCA)
@app.route('/query-image', methods=['POST'])
def query_image():
    if 'file' not in request.files:
        return jsonify({"error": "Gambar query tidak ditemukan!"}), 400

    file = request.files['file']
    filename = secure_filename(file.filename)
    query_path = os.path.join(QUERY_FOLDER, filename)
    file.save(query_path)

    # Proses query
    image_size = (64, 64)  # Ukuran gambar (resizing)
    k = 10  # Jumlah komponen utama
    result, execution_time = process_image_query(query_path, DATASET_FOLDER, image_size, k)

    return jsonify({
        "query_image": filename,
        "results": result,
        "execution_time_ms": execution_time
    })

# Placeholder untuk Query Audio
@app.route('/query-audio', methods=['POST'])
def query_audio():
    return jsonify({"message": "Fitur query audio belum diimplementasi."})

# Menjalankan Aplikasi
if __name__ == '__main__':
    app.run(debug=True)
