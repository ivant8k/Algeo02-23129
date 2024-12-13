import tkinter as tk
from tkinter import filedialog, messagebox
import sys
import os
from PIL import Image, ImageTk

# Tambahkan folder src ke PYTHONPATH
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Import modul dari backend
from backend.audio.main_audio import audioMain
from backend.image.imgtools import process_image_query, load_mapper

# Default settings
IMAGE_SIZE = (64, 64)
K = 20

# Global variables
dataset_folder = ""
mapper_path = ""
query_image_path = ""
audio_query_path = ""

# GUI Functions
def upload_dataset():
    global dataset_folder
    folder = filedialog.askdirectory(title="Pilih Folder Dataset Gambar")
    if folder:
        dataset_folder = folder
        lbl_dataset.config(text=f"Dataset: {os.path.basename(folder)}")
        messagebox.showinfo("Dataset Terunggah", f"Dataset berhasil dipilih: {folder}")

def upload_mapper():
    global mapper_path
    file = filedialog.askopenfilename(title="Pilih File Mapper", filetypes=[("JSON/TXT Files", "*.json *.txt")])
    if file:
        mapper_path = file
        lbl_mapper.config(text=f"Mapper: {os.path.basename(file)}")
        messagebox.showinfo("Mapper Terunggah", f"Mapper berhasil dipilih: {file}")

def upload_query_image():
    global query_image_path
    file = filedialog.askopenfilename(title="Pilih Gambar Query", filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
    if file:
        query_image_path = file
        lbl_query.config(text=f"Query Image: {os.path.basename(file)}")
        messagebox.showinfo("Gambar Query Terunggah", f"Gambar query berhasil dipilih: {file}")
def upload_audio():
    global audio_query_path
    file = filedialog.askopenfilename(title="Pilih File Audio Query", filetypes=[("MIDI Files", "*.midi *.mid")])
    if file:
        audio_query_path = file
        lbl_audio_query.config(text=f"Audio Query: {os.path.basename(file)}")
        messagebox.showinfo("Audio Query Terunggah", f"Audio query berhasil dipilih: {file}")

def run_program():
    global dataset_folder, mapper_path, query_image_path, audio_query_path
    if not dataset_folder or not mapper_path:
        messagebox.showerror("Error", "Pastikan dataset dan mapper telah diunggah.")
        return

    try:
        if query_image_path:
            # Jalankan pencarian berbasis gambar
            result, execution_time = process_image_query(
                query_image_path,
                dataset_folder,
                IMAGE_SIZE,
                K,
                mapper_path
            )
            display_results(result, execution_time, is_audio=False)
        elif audio_query_path:
            # Jalankan pencarian berbasis audio
            result = audioMain(audio_query_path)
            display_results(result, 0, is_audio=True)  # AudioMain tidak memberikan waktu eksekusi
        else:
            messagebox.showerror("Error", "Pilih file query gambar atau audio.")
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

def display_results(result, execution_time, is_audio):
    result_window = tk.Toplevel(root)
    result_window.title("Hasil Pencarian")
    if not is_audio:
        tk.Label(result_window, text=f"Waktu Eksekusi: {execution_time:.2f} ms", font=("Arial", 12, "bold")).pack(pady=10)
        for idx, res in enumerate(result, start=1):
            tk.Label(result_window, text=f"#{idx}: {res['filename']} (Audio: {res['audio']}) - Jarak: {res['distance']:.2f}").pack()
    else:
        tk.Label(result_window, text="Hasil Pencarian Audio", font=("Arial", 12, "bold")).pack(pady=10)
        for idx, (audio_file, similarity) in enumerate(result.items(), start=1):
            tk.Label(result_window, text=f"#{idx}: {audio_file} - Similarity: {similarity*100:.2f}%").pack()

# GUI Layout
root = tk.Tk()
root.title("PCA Album Finder")
root.geometry("500x400")

tk.Label(root, text="PCA Album Finder", font=("Arial", 16, "bold")).pack(pady=10)

# Dataset Upload
tk.Button(root, text="Unggah Dataset Gambar", command=upload_dataset).pack(pady=5)
lbl_dataset = tk.Label(root, text="Dataset: Belum dipilih")
lbl_dataset.pack()

# Mapper Upload
tk.Button(root, text="Unggah Mapper (JSON/TXT)", command=upload_mapper).pack(pady=5)
lbl_mapper = tk.Label(root, text="Mapper: Belum dipilih")
lbl_mapper.pack()

# Query Image Upload
tk.Button(root, text="Unggah Gambar Query", command=upload_query_image).pack(pady=5)
lbl_query = tk.Label(root, text="Query Image: Belum dipilih")
lbl_query.pack()
tk.Button(root, text="Unggah Audio Query", command=upload_audio).pack(pady=5)
lbl_audio_query = tk.Label(root, text="Audio Query: Belum dipilih")
lbl_audio_query.pack()
# Run Button
tk.Button(root, text="Jalankan Program", command=run_program, bg="green", fg="white", font=("Arial", 12, "bold")).pack(pady=20)

root.mainloop()
