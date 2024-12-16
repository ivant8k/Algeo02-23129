import os
import sys
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import zipfile
import rarfile
import shutil

# Tambahkan src ke PYTHONPATH
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Import modul backend
from backend.image.imgtools import process_image_query
from backend.audio.main_audio import process_audio_query

# Flask Config
app = Flask(
    __name__,
    template_folder=os.path.join("frontend", "templates"),
    static_folder=os.path.join("frontend", "static")
)
# Gunakan folder `static/uploads` untuk menyimpan file statis
app.config['UPLOAD_FOLDER'] = os.path.join(app.static_folder, 'uploads')
app.secret_key = "supersecretkey"

ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg'}
ALLOWED_AUDIO_EXTENSIONS = {'wav', 'mp3', 'midi'}
ALLOWED_MAPPER_EXTENSIONS = {'json', 'txt'}
ALLOWED_COMPRESSED_EXTENSIONS = {'zip', 'rar'}

# Helpers
def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def extract_compressed(file_path, extract_to):
    """Ekstrak file zip atau rar dengan debugging dan pemindahan file langsung."""
    print(f"Extracting {file_path} to {extract_to}")
    os.makedirs(extract_to, exist_ok=True)

    if file_path.endswith('.zip'):
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
    elif file_path.endswith('.rar'):
        with rarfile.RarFile(file_path, 'r') as rar_ref:
            rar_ref.extractall(extract_to)
    else:
        raise ValueError("Unsupported compressed file format.")

def move_files_to_static_folder(temp_folder, target_folder):
    """Pindahkan file dari folder sementara ke folder target di static."""
    for root, _, files in os.walk(temp_folder):
        for file in files:
            src_path = os.path.join(root, file)
            dst_path = os.path.join(target_folder, file)
            shutil.move(src_path, dst_path)
            print(f"Moved {src_path} to {dst_path}")

def clean_non_image_files(folder):
    """Hapus file non-gambar dari folder."""
    for file in os.listdir(folder):
        if not allowed_file(file, ALLOWED_IMAGE_EXTENSIONS):
            file_path = os.path.join(folder, file)
            if os.path.isfile(file_path):
                os.remove(file_path)

def debug_folder_contents(folder_path, folder_name=""):
    """Debug untuk memeriksa isi folder."""
    print(f"Debug: Mengakses folder {folder_name}: {folder_path}")
    if not os.path.exists(folder_path):
        print(f"Debug: Folder {folder_path} tidak ditemukan!")
    elif len(os.listdir(folder_path)) == 0:
        print(f"Debug: Folder {folder_path} kosong.")
    else:
        print(f"Debug: Folder {folder_path} berisi {os.listdir(folder_path)}")

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        image_files = request.files.getlist('image_dataset')
        audio_files = request.files.getlist('audio_dataset')
        mapper_file = request.files.get('mapper')

        # Validasi mapper
        if mapper_file and allowed_file(mapper_file.filename, ALLOWED_MAPPER_EXTENSIONS):
            mapper_filename = secure_filename(mapper_file.filename)
            mapper_path = os.path.join(app.config['UPLOAD_FOLDER'], 'mapper', mapper_filename)
            os.makedirs(os.path.dirname(mapper_path), exist_ok=True)
            mapper_file.save(mapper_path)
        else:
            flash("Invalid mapper file. Please upload .json or .txt format.", "danger")
            return redirect(request.url)

        # Proses dataset gambar
        if image_files:
            temp_image_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_images')
            target_image_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'images')
            os.makedirs(temp_image_folder, exist_ok=True)
            os.makedirs(target_image_folder, exist_ok=True)

            for image_file in image_files:
                filename = secure_filename(image_file.filename)
                filepath = os.path.join(temp_image_folder, filename)

                if filename.lower().endswith(('.zip', '.rar')):
                    image_file.save(filepath)
                    extract_compressed(filepath, temp_image_folder)
                    os.remove(filepath)
                elif allowed_file(filename, ALLOWED_IMAGE_EXTENSIONS):
                    image_file.save(filepath)

            move_files_to_static_folder(temp_image_folder, target_image_folder)
            shutil.rmtree(temp_image_folder)  # Hapus folder sementara
            debug_folder_contents(target_image_folder, "images")

        # Proses dataset audio
        if audio_files:
            temp_audio_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_audios')
            target_audio_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'audios')
            os.makedirs(temp_audio_folder, exist_ok=True)
            os.makedirs(target_audio_folder, exist_ok=True)

            for audio_file in audio_files:
                filename = secure_filename(audio_file.filename)
                filepath = os.path.join(temp_audio_folder, filename)

                if filename.lower().endswith(('.zip', '.rar')):
                    audio_file.save(filepath)
                    extract_compressed(filepath, temp_audio_folder)
                    os.remove(filepath)
                elif allowed_file(filename, ALLOWED_AUDIO_EXTENSIONS):
                    audio_file.save(filepath)

            move_files_to_static_folder(temp_audio_folder, target_audio_folder)
            shutil.rmtree(temp_audio_folder)  # Hapus folder sementara
            debug_folder_contents(target_audio_folder, "audio")

        flash("Datasets and mapper uploaded successfully.", "success")
        return redirect(url_for('query'))

    return render_template('upload.html')

@app.route('/query', methods=['GET', 'POST'])
def query():
    if request.method == 'POST':
        query_type = request.form.get('query_type')
        query_file = request.files.get('query_file')

        if query_file:
            query_filename = secure_filename(query_file.filename)
            query_path = os.path.join(app.config['UPLOAD_FOLDER'], 'query', query_filename)
            os.makedirs(os.path.dirname(query_path), exist_ok=True)
            query_file.save(query_path)

            if query_type == 'image':
                dataset_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'images')
                mapper_path = os.path.join(app.config['UPLOAD_FOLDER'], 'mapper', 'mapper.json')
                debug_folder_contents(dataset_folder, "images")

                results, execution_time = process_image_query(query_path, dataset_folder, (64, 64), 20, mapper_path)
                print("Debug: PCA Results Sent to Template:", results)
                return render_template('result.html', results=results, execution_time=execution_time)

            elif query_type == 'audio':
                dataset_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'audios')
                mapper_path = os.path.join(app.config['UPLOAD_FOLDER'], 'mapper', 'mapper.json')
                debug_folder_contents(dataset_folder, "audio")

                results, execution_time = process_audio_query(query_path, dataset_folder, mapper_path, tuning_values=None)
                
                return render_template('result.html', results=results, execution_time=execution_time)

        flash("Please upload a valid file for query.", "danger")
    return render_template('query.html')

@app.route('/result', methods=['GET'])
def result():
    return render_template('result.html')

if __name__ == '__main__':
    app.run(debug=True)
