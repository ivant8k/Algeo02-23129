from PIL import Image
import os
import time
import numpy as np
import matplotlib.pyplot as plt

# =====================================================================
# STEP 1: Image Processing and Loading
# =====================================================================

# Fungsi untuk mengubah gambar RGB menjadi grayscale
# Rumus digunakan: I(x, y) = 0.2989*R(x, y) + 0.587*G(x, y) + 0.114*B(x, y)
def rgbToGrayscale(RGBImage):
    width, height = RGBImage.size

    # Inisialisasi matriks grayscale
    matrix = [[0 for i in range(width)] for j in range(height)]
    
    # Iterasi setiap piksel untuk menghitung nilai grayscale
    for i in range(height):
        for j in range(width):
            r, g, b = RGBImage.getpixel((j, i))
            gscalevalue = int(0.2989 * r + 0.587 * g + 0.114 * b)  # Grayscale formula
            matrix[i][j] = gscalevalue
    
    return matrix

# Fungsi untuk mengubah ukuran gambar secara manual
# Menggunakan metode nearest neighbor scaling
def resize_image_manual(image_matrix, new_width, new_height):
    old_height, old_width = len(image_matrix), len(image_matrix[0])
    resized_matrix = [[0 for _ in range(new_width)] for _ in range(new_height)]
    
    # Hitung rasio skala
    for i in range(new_height):
        for j in range(new_width):
            old_x = int(j * old_width / new_width)
            old_y = int(i * old_height / new_height)
            resized_matrix[i][j] = image_matrix[old_y][old_x]
    
    return resized_matrix

# Fungsi untuk mengubah matriks grayscale 2D menjadi vektor 1D
# Diperlukan untuk PCA (operasi matriks lebih mudah dengan vektor 1D)
def grayscale_to_1d_vector(grayscale_matrix):
    return [pixel for row in grayscale_matrix for pixel in row]

# Fungsi untuk memuat semua gambar dari folder dataset
# Output: Daftar tuple (gambar asli, matriks grayscale yang telah di-resize)
def load_images_from_folder(folder, size):
    images = []
    for filename in os.listdir(folder):
        img = Image.open(os.path.join(folder, filename))  # Load gambar
        if img is not None:
            # Ubah menjadi grayscale, resize, lalu tambahkan ke list
            grayscale_matrix = rgbToGrayscale(img)
            resized_matrix = resize_image_manual(grayscale_matrix, size[0], size[1])
            images.append((img, resized_matrix))
    return images

# =====================================================================
# STEP 2: Data Centering (Standardization)
# =====================================================================

# Fungsi untuk menghitung rata-rata piksel dari semua gambar pada dataset
def calculate_pixel_averages(images):
    width, height = len(images[0][1][0]), len(images[0][1])  # Dimensi gambar
    N = len(images)  # Jumlah gambar
    pixel_sums = [[0 for _ in range(width)] for _ in range(height)]  # Inisialisasi
    
    # Iterasi setiap gambar untuk menjumlahkan nilai piksel
    for _, img in images:
        for i in range(height):
            for j in range(width):
                pixel_sums[i][j] += img[i][j]
    
    # Hitung rata-rata piksel
    pixel_averages = [[pixel_sums[i][j] / N for j in range(width)] for i in range(height)]
    return pixel_averages

# Fungsi untuk melakukan standarisasi gambar (mengurangi rata-rata piksel)
def standardize_images(images, pixel_averages):
    standardized_images = []
    for _, img in images:
        width, height = len(img[0]), len(img)
        standardized_matrix = [[0 for _ in range(width)] for _ in range(height)]
        
        # Kurangi rata-rata piksel
        for i in range(height):
            for j in range(width):
                standardized_matrix[i][j] = img[i][j] - pixel_averages[i][j]
        
        # Ubah menjadi vektor 1D dan simpan
        standardized_images.append(grayscale_to_1d_vector(standardized_matrix))
    return standardized_images

# =====================================================================
# STEP 3: PCA Computation Using SVD
# =====================================================================

# Fungsi untuk menghitung transpose matriks secara manual
def transpose(Mtx):
    h = len(Mtx)  # Jumlah baris
    w = len(Mtx[0])  # Jumlah kolom
    MtxT = [[0 for _ in range(h)] for _ in range(w)]  # Inisialisasi transpose
    for i in range(h):
        for j in range(w):
            MtxT[j][i] = Mtx[i][j]
    return MtxT

# Fungsi untuk menghitung matriks kovarian
# Rumus digunakan: C = (1/N) X'^T X'
def hitung_kovarian(data):
    N = len(data)  # Jumlah sampel
    transposed_data = transpose(data)
    cov_matrix = np.dot(transposed_data, data) / N  # Matriks kovarian
    return cov_matrix

# Fungsi untuk menghitung eigenvalue dan eigenvector secara iteratif
# Rumus: AX = λX
def calculate_eigendecomposition(C):
    n = len(C)
    eigenvalues = np.zeros(n)
    eigenvectors = np.zeros((n, n))

    C_remaining = np.array(C) # Salin matriks kovarian

    for i in range(10):  # Iterasi untuk setiap eigenvector
        print(f"Calculating eigenvector {i+1}")
        v = np.random.rand(n) # Inisialisasi vektor acak
        v = v / np.linalg.norm(v)  # Normalisasi

        for _ in range(100): # Iterasi maksimum 100 kali
            Cv = np.dot(C_remaining, v) # Kalikan matriks dengan vektor
            lambda_i = np.dot(v, Cv) / np.dot(v, v)# Hitung eigenvalue

            v_new = Cv / np.linalg.norm(Cv) # Normalisasi eigenvector baru
            # Periksa konvergensi
            if np.allclose(v, v_new, rtol=1e-6):
                break
            v = v_new

        eigenvalues[i] = lambda_i # Simpan eigenvalue
        eigenvectors[:, i] = v # Simpan eigenvector
        # Kurangi kontribusi eigenvector dari matriks
        C_remaining = C_remaining - lambda_i * np.outer(v, v)
    # Urutkan eigenvalue dan eigenvector
    idx = eigenvalues.argsort()[::-1]
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]

    return eigenvectors, eigenvalues

# Fungsi untuk menghitung SVD
def calculate_svd(C, k):
    U, S = calculate_eigendecomposition(C)  # Hitung eigenvalue dan eigenvector
    Uk = U[:, :k]  # Ambil k eigenvector teratas
    return Uk

# =====================================================================
# STEP 4: Similarity Calculation
# =====================================================================

# Fungsi untuk memproyeksikan gambar query ke ruang PCA
def project_query_image(query_image_path, pixel_averages, Uk, image_size):
    img = Image.open(query_image_path)
    grayscale_matrix = rgbToGrayscale(img)
    resized_matrix = resize_image_manual(grayscale_matrix, image_size[0], image_size[1])
    
    standardized_matrix = [[resized_matrix[i][j] - pixel_averages[i][j] for j in range(image_size[0])] for i in range(image_size[1])]
    standardized_vector = grayscale_to_1d_vector(standardized_matrix)
    
    q = np.dot(standardized_vector, Uk)  # Proyeksikan gambar query
    return img, q

# Fungsi untuk menghitung jarak Euclidean antara query dan dataset
def calculate_euclidean_distances(query_vector, projected_data):
    distances = []
    for i, z in enumerate(projected_data):
        distance = np.linalg.norm(query_vector - z)  # Hitung jarak Euclidean
        distances.append((i, distance))
    return distances

# Fungsi untuk mengurutkan jarak berdasarkan nilai terkecil
def sort_by_distance(distances):
    return sorted(distances, key=lambda x: x[1])
# =====================================================================
# Retrieval and Output
# =====================================================================
# Folder untuk menyimpan dataset
# Lokasi folder kerja berdasarkan struktur Anda
DATASET_FOLDER = "test/dataset"
QUERY_FOLDER = "test/query"
MAPPER_PATH = "test/mapper.json"

# Fungsi untuk memproses query gambar dengan PCA
def process_image_query(query_image_path, dataset_folder, image_size, k):
    """
    Proses query gambar menggunakan PCA.

    Parameters:
    - query_image_path: str, path gambar query.
    - dataset_folder: str, folder dataset gambar.
    - image_size: tuple, ukuran gambar (width, height).
    - k: int, jumlah komponen utama PCA.

    Returns:
    - result: list of dict, hasil query berupa gambar mirip dan jaraknya.
    - execution_time: float, waktu eksekusi dalam milidetik.
    """
    # Mulai timer
    start_time = time.time()

    # Load dataset gambar
    images = load_images_from_folder(dataset_folder, image_size)
    pixel_averages = calculate_pixel_averages(images)
    standardized_images = standardize_images(images, pixel_averages)
    cov_matrix = hitung_kovarian(standardized_images)
    Uk = calculate_svd(cov_matrix, k)
    Z = np.dot(standardized_images, Uk)  # Proyeksikan dataset

    # Proses query image
    query_img, q = project_query_image(query_image_path, pixel_averages, Uk, image_size)
    distances = calculate_euclidean_distances(q, Z)
    sorted_distances = sort_by_distance(distances)

    # Ambil hasil dengan threshold (misalnya 20% terdekat)
    threshold_distance = np.percentile([d for _, d in sorted_distances], 20)
    similar_images_indices = [i for i, d in sorted_distances if d <= threshold_distance]

    # Format hasil
    result = []
    for idx in similar_images_indices:
        result.append({
            "image_index": idx,
            "distance": sorted_distances[idx][1],
            "filename": os.listdir(dataset_folder)[idx]
        })

    # Hitung waktu eksekusi
    execution_time = (time.time() - start_time) * 1000  # Dalam milidetik
    return result, execution_time