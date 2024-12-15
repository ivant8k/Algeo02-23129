from flask import Flask, request, jsonify
import os
from backend.image.imgtools import process_image_query, load_mapper
from backend.audio.main_audio import process_audio_query

# Inisialisasi Flask app
app = Flask(__name__)

# Variabel untuk menyimpan dataset dan mapper
DATASET_IMAGE_FOLDER = "uploads/images"
DATASET_AUDIO_FOLDER = "uploads/audios"
MAPPER_PATH = None

# Pastikan folder untuk dataset ada
os.makedirs(DATASET_IMAGE_FOLDER, exist_ok=True)
os.makedirs(DATASET_AUDIO_FOLDER, exist_ok=True)

@app.route('/status', methods=['GET'])
def status():
    """Endpoint untuk memeriksa status server"""
    return jsonify({"status": "Server berjalan", "message": "API siap digunakan"}), 200

@app.route('/upload-datasets', methods=['POST'])
def upload_datasets():
    """Endpoint untuk mengunggah dataset gambar dan audio"""
    image_files = request.files.getlist('image_files')
    audio_files = request.files.getlist('audio_files')

    # Simpan gambar
    for file in image_files:
        file.save(os.path.join(DATASET_IMAGE_FOLDER, file.filename))

    # Simpan audio
    for file in audio_files:
        file.save(os.path.join(DATASET_AUDIO_FOLDER, file.filename))

    return jsonify({"message": "Datasets berhasil diunggah"}), 200

@app.route('/upload-mapper', methods=['POST'])
def upload_mapper():
    """Endpoint untuk mengunggah file mapper"""
    global MAPPER_PATH
    mapper_file = request.files.get('mapper_file')
    if not mapper_file:
        return jsonify({"error": "Mapper file tidak ditemukan"}), 400

    # Simpan mapper
    mapper_path = os.path.join("uploads", mapper_file.filename)
    mapper_file.save(mapper_path)
    MAPPER_PATH = mapper_path

    return jsonify({"message": "Mapper berhasil diunggah", "path": MAPPER_PATH}), 200

@app.route('/query', methods=['POST'])
def query():
    """Endpoint untuk menjalankan pencarian berdasarkan query (gambar/audio)"""
    query_file = request.files.get('query_file')
    is_audio = request.form.get('is_audio') == 'true'
    k = int(request.form.get('k', 20))  # Default jumlah komponen PCA adalah 20

    if not query_file:
        return jsonify({"error": "Query file tidak ditemukan"}), 400

    # Simpan file query sementara
    query_path = os.path.join("uploads", "query", query_file.filename)
    os.makedirs(os.path.dirname(query_path), exist_ok=True)
    query_file.save(query_path)

    # Validasi mapper
    if not MAPPER_PATH:
        return jsonify({"error": "Mapper belum diunggah"}), 400

    # Jalankan pencarian
    try:
        if is_audio:
            result, execution_time = process_audio_query(
                query_path, DATASET_AUDIO_FOLDER, MAPPER_PATH
            )
        else:
            result, execution_time = process_image_query(
                query_path, DATASET_IMAGE_FOLDER, (64, 64), k, MAPPER_PATH
            )

        return jsonify({
            "query": query_file.filename,
            "results": result,
            "execution_time": execution_time
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
