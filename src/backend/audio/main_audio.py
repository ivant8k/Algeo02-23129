import os
from decimal import Decimal
from backend.audio.mir.audio import Audio
from backend.image.imgtools import load_mapper

def process_audio_query(test_file_path, dataset_folder, mapper_path=None, tuning_values=None):
    """
    Proses query audio untuk mencari similaritas dengan dataset.

    Parameters:
    - test_file_path: str, path file audio query.
    - dataset_folder: str, folder dataset audio.
    - mapper_path: str, path ke file mapper (opsional).
    - tuning_values: list[int], bobot untuk ATB, RTB, FTB (default: [20, 40, 40]).

    Returns:
    - result: list of dict, hasil query berupa audio mirip dan gambar terkait.
    - execution_time: float, waktu eksekusi dalam milidetik.
    """
    import time

    if tuning_values is None:
        tuning_values = [20, 40, 40]  # Bobot default

    # Mulai timer
    start_time = time.time()

    # Pastikan file query ada
    if not os.path.isfile(test_file_path):
        raise FileNotFoundError(f"Query file tidak ditemukan: {test_file_path}")

    # Pastikan folder dataset ada
    if not os.path.isdir(dataset_folder):
        raise FileNotFoundError(f"Folder dataset tidak ditemukan: {dataset_folder}")

    # Muat mapper
    mapper = load_mapper(mapper_path) if mapper_path else {}

    # Buka file audio uji
    audio_test = Audio(test_file_path)
    window_size = audio_test.size
    window_step = audio_test.step

    # Sederhanakan audio uji dengan mengambil 1 window saja
    audio_test.beats = [audio_test.beats[len(audio_test.beats) // 2 + 1]]

    # Iterasi setiap file dalam folder dataset
    similarity_results = []
    for file_dataset in os.listdir(dataset_folder):
        dataset_file_path = os.path.join(dataset_folder, file_dataset)

        # Pastikan file dataset adalah file valid
        if not os.path.isfile(dataset_file_path):
            print(f"Skipping non-file entry: {dataset_file_path}")
            continue
        print(f"Processing audio file: {dataset_file_path}")
        # Buka file audio dataset
        audio_dataset = Audio(dataset_file_path, window_size, window_step)

        # Mencari similaritas
        similarity_value = audio_test.compare(audio_dataset, tuning_values, cli=False)

        # Tambahkan hasil ke list
        similarity_results.append({
            "filename": file_dataset,  # Nama file audio (sama seperti PCA, ganti "audio" menjadi "filename")
            "similarity": similarity_value * 100,  # Similaritas dalam persen
            "image_path": f"/static/uploads/images/{mapper.get(os.path.basename(file_dataset), 'Unknown')}",  # Path gambar terkait
            "audio": file_dataset  # Nama file audio
        })

        print(f"Debug: Audio Query Result - Audio: {file_dataset}, Image: {mapper.get(os.path.basename(file_dataset), 'Unknown')}")

        print(f"Debug: Mapper Match for {file_dataset}: {mapper.get(os.path.basename(file_dataset), 'No image available')}")
    # Urutkan hasil berdasarkan similaritas tertinggi
    similarity_results.sort(key=lambda x: x["similarity"], reverse=True)

    # Hitung waktu eksekusi
    execution_time = (time.time() - start_time) * 1000  # Dalam milidetik

    return similarity_results, execution_time