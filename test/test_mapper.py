import sys
import os

# Tambahkan folder src ke PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from backend.generate_mapper import generate_mapper


# Path dataset
audio_folder = "test/audiodata"
image_folder = "test/imgdata"
txt_output = "test/mapper_test.txt"
json_output = "test/mapper_test.json"

# Jalankan fungsi
try:
    generate_mapper(audio_folder, image_folder, txt_output, json_output)
    print(f"Mapper berhasil dibuat!\n- TXT: {txt_output}\n- JSON: {json_output}")
except Exception as e:
    print(f"Terjadi kesalahan: {e}")
