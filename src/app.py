import os
import sys
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import zipfile
import rarfile

# Tambahkan src ke PYTHONPATH
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Import modul backend
from backend.image.imgtools import process_image_query
from backend.audio.main_audio import process_audio_query
import shutil   # Untuk menyalin folder langsung

def extract_compressed_file(filepath, extract_to):
    """Ekstrak file ZIP atau RAR ke folder target."""
    if zipfile.is_zipfile(filepath):
        with zipfile.ZipFile(filepath, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
    elif rarfile.is_rarfile(filepath):
        with rarfile.RarFile(filepath, 'r') as rar_ref:
            rar_ref.extractall(extract_to)
    else:
        raise ValueError("Unsupported compressed file format.")
# Konfigurasi aplikasi Flask
app = Flask(
    __name__,
    template_folder=os.path.join("frontend", "templates"),
    static_folder=os.path.join("frontend", "static")
)
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
app.secret_key = "supersecretkey"

ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg'}
ALLOWED_AUDIO_EXTENSIONS = {'wav', 'mp3', 'midi'}
ALLOWED_MAPPER_EXTENSIONS = {'json', 'txt'}
ALLOWED_COMPRESSED_EXTENSIONS = {'zip', 'rar'}

# Helpers
def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def extract_compressed(file_path, extract_to):
    """Extract zip or rar files."""
    if file_path.endswith('.zip'):
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
    elif file_path.endswith('.rar'):
        with rarfile.RarFile(file_path, 'r') as rar_ref:
            rar_ref.extractall(extract_to)

# Routes
@app.route('/')
def home():
    return render_template('home.html')
@app.route('/upload', methods=['GET','POST'])
def upload():
    print(f"Method received: {request.method}")
    #try:
    if request.method == 'POST':
        # Ambil semua file yang diunggah
        image_files = request.files.getlist('image_dataset')
        audio_files = request.files.getlist('audio_dataset')
        mapper_file = request.files.get('mapper')

        # Validasi mapper
        if mapper_file and allowed_file(mapper_file.filename, ALLOWED_MAPPER_EXTENSIONS):
            mapper_filename = secure_filename(mapper_file.filename)
            mapper_file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'mapper', mapper_filename))
        else:
            flash("Invalid mapper file. Please upload .json or .txt format.", "danger")
            return redirect(request.url)

        # Proses dataset gambar
        if image_files:
            for image_file in image_files:
                filename = secure_filename(image_file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'images', filename)

                # Tangani file ZIP/RAR
                if filename.lower().endswith(('.zip', '.rar')):
                    temp_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    image_file.save(temp_path)
                    extract_compressed_file(temp_path, os.path.join(app.config['UPLOAD_FOLDER'], 'images'))
                    os.remove(temp_path)  # Hapus file ZIP/RAR setelah ekstraksi
                elif allowed_file(filename, ALLOWED_IMAGE_EXTENSIONS):
                    image_file.save(filepath)
                else:
                    flash(f"Invalid image file: {filename}", "danger")
                    return redirect(request.url)

        # Proses dataset audio
        if audio_files:
            for audio_file in audio_files:
                filename = secure_filename(audio_file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'audios', filename)

                # Tangani file ZIP/RAR
                if filename.lower().endswith(('.zip', '.rar')):
                    temp_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    audio_file.save(temp_path)
                    extract_compressed_file(temp_path, os.path.join(app.config['UPLOAD_FOLDER'], 'audios'))
                    os.remove(temp_path)  # Hapus file ZIP/RAR setelah ekstraksi
                elif allowed_file(filename, ALLOWED_AUDIO_EXTENSIONS):
                    audio_file.save(filepath)
                else:
                    flash(f"Invalid audio file: {filename}", "danger")
                    return redirect(request.url)

        flash("Datasets and mapper uploaded successfully.", "success")
        return redirect(url_for('query'))
    return render_template('upload.html')
    #except Exception as e:
    #    flash(f"Terjadi kesalahan: {str(e)}", "danger")
    #    return redirect(request.url)
'''
@app.route('/query', methods=['GET', 'POST'])
def query():
    if request.method == 'POST':
        query_type = request.form['query_type']
        query_file = request.files.get('query_file')

        if query_file:
            query_filename = secure_filename(query_file.filename)
            query_path = os.path.join(app.config['UPLOAD_FOLDER'], 'query', query_filename)
            query_file.save(query_path)

            if query_type == 'image':
                # Proses query gambar
                dataset_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'images')
                mapper_path = os.path.join(app.config['UPLOAD_FOLDER'], 'mapper', 'mapper.json')  # Cek keberadaan mapper
                
                # Tambahkan pengecekan keberadaan mapper
                if not os.path.exists(mapper_path):
                    flash("Mapper file not found. Please upload mapper.json.", "danger")
                    return redirect(url_for('upload'))
                
                # Jalankan proses
                try:
                    results, execution_time = process_image_query(query_path, dataset_folder, (64, 64), 20, mapper_path)
                except Exception as e:
                    flash(f"Error during PCA processing: {str(e)}", "danger")
                    return redirect(request.url)

                return render_template('result.html', results=results, execution_time=execution_time)

            elif query_type == 'audio':
                # Proses query audio
                dataset_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'audios')
                mapper_path = os.path.join(app.config['UPLOAD_FOLDER'], 'mapper', 'mapper.json')  # Cek keberadaan mapper
                
                # Tambahkan pengecekan keberadaan mapper
                if not os.path.exists(mapper_path):
                    flash("Mapper file not found. Please upload mapper.json.", "danger")
                    return redirect(url_for('upload'))
                
                # Jalankan proses
                try:
                    results, execution_time = process_audio_query(query_path, dataset_folder, mapper_path)
                except Exception as e:
                    flash(f"Error during audio query processing: {str(e)}", "danger")
                    return redirect(request.url)

                return render_template('result.html', results=results, execution_time=execution_time)

        else:
            flash("Please upload a valid file for query.", "danger")
            return redirect(request.url)
    return render_template('query.html')
'''
@app.route('/query', methods=['GET', 'POST'])
def query():
    if request.method == 'POST':
        query_type = request.form.get('query_type')
        query_file = request.files.get('query_file')

        if query_file:
            query_filename = secure_filename(query_file.filename)
            query_path = os.path.join(app.config['UPLOAD_FOLDER'], 'query', query_filename)
            query_file.save(query_path)  # Simpan file query
            print(f"Query file saved at: {query_path}")

            if query_type == 'image':
                dataset_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'images')
                mapper_path = os.path.join(app.config['UPLOAD_FOLDER'], 'mapper', 'mapper.json')
                #if not os.path.exists(mapper_path):
               #     flash("Mapper file not found. Please upload mapper.json.", "danger")
               #     return redirect(url_for('upload'))
                results, execution_time = process_image_query(query_path, dataset_folder, (64, 64), 20, mapper_path)
                return render_template('result.html', results=results, execution_time=execution_time)
                #try:
                #    results, execution_time = process_image_query(query_path, dataset_folder, (64, 64), 20, mapper_path)
                #    return render_template('result.html', results=results, execution_time=execution_time)
               # except Exception as e:
                 #   flash(f"Error during PCA processing: {str(e)}", "danger")
                #    return redirect(request.url)

            elif query_type == 'audio':
                dataset_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'audios')
                mapper_path = os.path.join(app.config['UPLOAD_FOLDER'], 'mapper', 'mapper.json')
                if not os.path.exists(mapper_path):
                    flash("Mapper file not found. Please upload mapper.json.", "danger")
                    return redirect(url_for('upload'))

                try:
                    results, execution_time = process_audio_query(query_path, dataset_folder, mapper_path)
                    print(f"Results: {results}")
                    return render_template('result.html', results=results, execution_time=execution_time)
                except Exception as e:
                    flash(f"Error during Query by Humming: {str(e)}", "danger")
                    return redirect(request.url)
        else:
            flash("Please upload a valid file for query.", "danger")
            return redirect(request.url)
    return render_template('query.html')


@app.route('/result', methods=['GET'])
def result():
    return render_template('result.html')

if __name__ == '__main__':
    # Buat folder uploads jika tidak ada
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'audios'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'images'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'mapper'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'query'), exist_ok=True)

    app.run(debug=True)
