import os
import sys
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import zipfile
import rarfile
import shutil
import patoolib

# Tambahkan src ke PYTHONPATH
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Import modul backend
from backend.image.imgtools import process_image_query
from backend.audio.main_audio import process_audio_query

# Fungsi untuk menghapus isi folder
def clean_folder(folder_path):
    """Menghapus semua file dalam folder, tetapi tidak folder itu sendiri."""
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path):  # Jika itu file
                    os.remove(file_path)
                elif os.path.isdir(file_path):  # Jika itu folder
                    shutil.rmtree(file_path)
                print(f"Deleted {file_path}")
            except Exception as e:
                print(f"Failed to delete {file_path}: {e}")
    else:
        print(f"Folder {folder_path} tidak ditemukan!")

# Membersihkan folder saat aplikasi dimulai
def clean_uploads():
    base_path = os.path.join(os.getcwd(), 'src', 'frontend', 'static', 'uploads')
    
    # Folder yang ingin dibersihkan
    folders_to_clean = ['audios', 'images', 'mapper', 'query']
    
    for folder in folders_to_clean:
        folder_path = os.path.join(base_path, folder)
        clean_folder(folder_path)

# Panggil clean_uploads saat aplikasi dimulai
clean_uploads()

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

def get_mapper_path():
    """Get the path of the mapper file, checking for both .json and .txt extensions"""
    mapper_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'mapper')
    
    # List all files in mapper folder
    if os.path.exists(mapper_folder):
        files = os.listdir(mapper_folder)
        for file in files:
            if file.endswith('.txt') or file.endswith('.json'):
                return os.path.join(mapper_folder, file)
    
    raise FileNotFoundError("No mapper file found (must be .txt or .json)")

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
        try:
            patoolib.extract_archive(file_path, outdir=extract_to)
            print(f"Successfully extracted .rar file: {file_path}")
        except Exception as e:
            print(f"Error extracting .rar file: {e}")
            raise ValueError("Failed to extract .rar file.")
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
            # Simpan dengan nama asli file
            mapper_path = os.path.join(app.config['UPLOAD_FOLDER'], 'mapper', mapper_filename)
            os.makedirs(os.path.dirname(mapper_path), exist_ok=True)
            mapper_file.save(mapper_path)
            print(f"Debug: Mapper saved as {mapper_path}")
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
            shutil.rmtree(temp_image_folder)
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
            shutil.rmtree(temp_audio_folder)
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

            try:
                # Get mapper path dynamically
                mapper_path = get_mapper_path()
                print(f"Debug: Using mapper file: {mapper_path}")

                if query_type == 'image':
                    dataset_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'images')
                    debug_folder_contents(dataset_folder, "images")

                    results, execution_time = process_image_query(query_path, dataset_folder, (64, 64), 20, mapper_path)
                    print("Debug: PCA Results Sent to Template:", results)
                    return render_template('result.html', results=results, execution_time=execution_time)

                elif query_type == 'audio':
                    dataset_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'audios')
                    debug_folder_contents(dataset_folder, "audio")

                    results, execution_time = process_audio_query(query_path, dataset_folder, mapper_path, tuning_values=None)
                    return render_template('result.html', results=results, execution_time=execution_time)

            except FileNotFoundError as e:
                flash(f"Error: {str(e)}", "danger")
                return redirect(url_for('query'))
            except Exception as e:
                print(f"Debug: Error processing query: {str(e)}")
                flash(f"Error processing query: {str(e)}", "danger")
                return redirect(url_for('query'))

        flash("Please upload a valid file for query.", "danger")
    return render_template('query.html')

@app.route('/result', methods=['GET'])
def result():
    return render_template('result.html')

if __name__ == '__main__':
    app.run(debug=True)