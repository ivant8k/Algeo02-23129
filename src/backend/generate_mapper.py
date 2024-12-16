import os
import json

def generate_mapper(audio_folder, image_folder, txt_output, json_output):
    """
    Fungsi untuk membuat mapper.txt dan mapper.json berdasarkan file di folder audio dan image.
    """
    audio_files = sorted(os.listdir(audio_folder))
    image_files = sorted(os.listdir(image_folder))

    # Pastikan jumlah file cocok
    if len(audio_files) != len(image_files):
        raise ValueError("Jumlah file audio dan gambar tidak sama!")

    # Buat mapper dalam format list of dictionaries
    mapper = [{"audio_file": audio, "pic_name": image} for audio, image in zip(audio_files, image_files)]

    # Simpan ke mapper.txt
    with open(txt_output, 'w') as f:
        f.write("audio_file       pic_name\n")
        for entry in mapper:
            f.write(f"{entry['audio_file']:<15} {entry['pic_name']}\n")

    # Simpan ke mapper.json
    with open(json_output, 'w') as f:
        json.dump(mapper, f, indent=4)

    print(f"Mapper berhasil dibuat di:\n- {txt_output}\n- {json_output}")

# Contoh penggunaan
if __name__ == "__main__":
    audio_folder = "test/audiodata"
    image_folder = "test/imgdata"
    txt_output = "test/mapper.txt"
    json_output = "test/mapper.json"

    generate_mapper(audio_folder, image_folder, txt_output, json_output)
