from flask import Flask, request, jsonify, render_template

# Inisialisasi Flask app
app = Flask(__name__)

# Halaman Utama
@app.route('/')
def home():
    return "Selamat datang di Information Retrieval System!"

# Endpoint Upload Dataset
@app.route('/upload-dataset', methods=['POST'])
def upload_dataset():
    # Dummy response untuk upload dataset
    if 'file' not in request.files:
        return jsonify({"error": "File tidak ditemukan dalam permintaan!"}), 400
    
    file = request.files['file']
    # Simpan file ke folder uploads (pastikan folder ada)
    file.save(f"uploads/{file.filename}")
    return jsonify({"message": f"File {file.filename} berhasil diunggah!"})

# Endpoint Dummy untuk Query Gambar
@app.route('/query-image', methods=['POST'])
def query_image():
    # Dummy response untuk query gambar
    return jsonify({"message": "Fitur query gambar akan segera tersedia."})

# Endpoint Dummy untuk Query Audio
@app.route('/query-audio', methods=['POST'])
def query_audio():
    # Dummy response untuk query audio
    return jsonify({"message": "Fitur query audio akan segera tersedia."})

# Menjalankan Aplikasi
if __name__ == '__main__':
    app.run(debug=True)
