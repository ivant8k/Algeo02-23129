import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import sys

# Tambahkan folder src ke PYTHONPATH
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Impor modul yang relevan
from backend.image.imgtools import process_image_query, load_mapper
from backend.audio.main_audio import process_audio_query

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Information Retrieval System")
        self.root.geometry("600x400")
        
        # Variabel untuk menyimpan file
        self.query_file = None
        self.dataset_image_folder = None
        self.dataset_audio_folder = None
        self.mapper_file = None

        # Frame untuk Input
        frame_input = tk.Frame(root)
        frame_input.pack(pady=20)

        tk.Button(frame_input, text="Unggah Query (Gambar/Audio)", command=self.upload_query).pack(pady=5)
        tk.Button(frame_input, text="Unggah Dataset Gambar", command=self.upload_dataset_image).pack(pady=5)
        tk.Button(frame_input, text="Unggah Dataset Audio", command=self.upload_dataset_audio).pack(pady=5)
        tk.Button(frame_input, text="Unggah Mapper", command=self.upload_mapper).pack(pady=5)

        # Frame untuk Eksekusi
        frame_action = tk.Frame(root)
        frame_action.pack(pady=20)
        tk.Button(frame_action, text="Jalankan Pencarian", command=self.run_query).pack()

        # Frame untuk Output
        self.frame_output = tk.Frame(root)
        self.frame_output.pack(pady=20)

    def upload_query(self):
        self.query_file = filedialog.askopenfilename(
            title="Pilih File Query (Gambar atau Audio)",
            filetypes=(("Gambar atau Audio", "*.jpg *.jpeg *.png *.midi"), ("Semua File", "*.*"))
        )
        messagebox.showinfo("Query File", f"File dipilih: {os.path.basename(self.query_file)}")

    def upload_dataset_image(self):
        self.dataset_image_folder = filedialog.askdirectory(title="Pilih Folder Dataset Gambar")
        messagebox.showinfo("Dataset Gambar", f"Folder dipilih: {self.dataset_image_folder}")

    def upload_dataset_audio(self):
        self.dataset_audio_folder = filedialog.askdirectory(title="Pilih Folder Dataset Audio")
        messagebox.showinfo("Dataset Audio", f"Folder dipilih: {self.dataset_audio_folder}")

    def upload_mapper(self):
        self.mapper_file = filedialog.askopenfilename(
            title="Pilih File Mapper (JSON atau TXT)",
            filetypes=(("File Mapper", "*.json *.txt"), ("Semua File", "*.*"))
        )
        messagebox.showinfo("Mapper File", f"File dipilih: {os.path.basename(self.mapper_file)}")

    def run_query(self):
        if not self.query_file or not self.dataset_image_folder or not self.dataset_audio_folder or not self.mapper_file:
            messagebox.showerror("Error", "Harap unggah semua file yang diperlukan!")
            return

        is_audio = self.query_file.endswith(".midi")

        # Hapus hasil sebelumnya
        for widget in self.frame_output.winfo_children():
            widget.destroy()

        # Jalankan pencarian
        try:
            if is_audio:
                result, execution_time = process_audio_query(
                    self.query_file,
                    self.dataset_audio_folder,
                    mapper_path=self.mapper_file
                )
            else:
                result, execution_time = process_image_query(
                    self.query_file,
                    self.dataset_image_folder,
                    (64, 64),  # Ukuran gambar
                    k=20,  # Jumlah principal component
                    mapper_path=self.mapper_file
                )

            self.display_results(result, execution_time, is_audio)

        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

    def display_results(self, result, execution_time, is_audio):
        tk.Label(self.frame_output, text=f"Waktu Eksekusi: {execution_time:.2f} ms", font=("Arial", 12, "bold")).pack(pady=10)

        if not is_audio:
            for idx, res in enumerate(result, start=1):
                frame = tk.Frame(self.frame_output)
                frame.pack(pady=5)

                # Tampilkan gambar
                image_path = os.path.join(self.dataset_image_folder, res["filename"])
                img = Image.open(image_path)
                img = img.resize((150, 150))
                img_tk = ImageTk.PhotoImage(img)

                lbl_image = tk.Label(frame, image=img_tk)
                lbl_image.image = img_tk  # Simpan referensi
                lbl_image.pack(side=tk.LEFT, padx=5)

                # Tampilkan informasi
                tk.Label(frame, text=f"#{idx}: {res['filename']}\nJarak: {res['distance']:.2f}").pack(side=tk.LEFT, padx=5)
        else:
            for idx, res in enumerate(result, start=1):
                frame = tk.Frame(self.frame_output)
                frame.pack(pady=5)

                # Tampilkan gambar terkait audio dari mapper
                mapped_image = res.get("image")
                if mapped_image:
                    image_path = os.path.join(self.dataset_image_folder, mapped_image)
                    try:
                        img = Image.open(image_path)
                        img = img.resize((150, 150))
                        img_tk = ImageTk.PhotoImage(img)

                        lbl_image = tk.Label(frame, image=img_tk)
                        lbl_image.image = img_tk  # Simpan referensi
                        lbl_image.pack(side=tk.LEFT, padx=5)
                    except FileNotFoundError:
                        tk.Label(frame, text="Gambar tidak ditemukan", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)

                # Tampilkan informasi audio
                tk.Label(frame, text=f"#{idx}: {res['filename']} - Similarity: {res['similarity']:.2f}%").pack(side=tk.LEFT, padx=5)

# Jalankan Aplikasi
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
