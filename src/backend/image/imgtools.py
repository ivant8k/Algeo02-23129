from PIL import Image
import os
import numpy as np

def rgbToGrayscale(RGBImage):
    width, height = RGBImage.size

    matrix = [[0 for i in range(width)] for j in range(height)]
    
    for i in range(height):
        for j in range(width):
            r, g, b = RGBImage.getpixel((j, i))
            gscalevalue = int(0.2989 * r + 0.587 * g + 0.114 * b)
            matrix[i][j] = gscalevalue
    
    return matrix

def resize_image_manual(image_matrix, new_width, new_height):
    """Resize gambar menggunakan metode nearest neighbor."""
    old_height, old_width = len(image_matrix), len(image_matrix[0])
    resized_matrix = [[0 for _ in range(new_width)] for _ in range(new_height)]
    
    for i in range(new_height):
        for j in range(new_width):
            # Skalakan koordinat berdasarkan rasio dimensi
            old_x = int(j * old_width / new_width)
            old_y = int(i * old_height / new_height)
            resized_matrix[i][j] = image_matrix[old_y][old_x]
    
    return resized_matrix

def grayscale_to_1d_vector(grayscale_matrix):
    return [pixel for row in grayscale_matrix for pixel in row]

def load_images_from_folder(folder, size):
    images = []
    for filename in os.listdir(folder):
        img = Image.open(os.path.join(folder, filename))
        if img is not None:
            grayscale_matrix = rgbToGrayscale(img)
            resized_matrix = resize_image_manual(grayscale_matrix, size[0], size[1])
            images.append(resized_matrix)
    return images

def calculate_pixel_averages(images):
    width, height = len(images[0][0]), len(images[0])
    N = len(images)
    pixel_sums = [[0 for _ in range(width)] for _ in range(height)]
    
    for img in images:
        for i in range(height):
            for j in range(width):
                pixel_sums[i][j] += img[i][j]
    
    pixel_averages = [[pixel_sums[i][j] / N for j in range(width)] for i in range(height)]
    return pixel_averages

def standardize_images(images, pixel_averages):
    standardized_images = []
    for img in images:
        width, height = len(img[0]), len(img)
        standardized_matrix = [[0 for _ in range(width)] for _ in range(height)]
        
        for i in range(height):
            for j in range(width):
                standardized_matrix[i][j] = img[i][j] - pixel_averages[i][j]
        
        standardized_images.append(grayscale_to_1d_vector(standardized_matrix))
    return standardized_images

def transpose(Mtx):
    h = len(Mtx)
    w = len(Mtx[0])
    MtxT = [[0 for _ in range(h)] for _ in range(w)]
    for i in range(h):
        for j in range(w):
            MtxT[j][i] = Mtx[i][j]
    return MtxT

def hitung_kovarian(data):
    N = len(data)
    transposed_data = transpose(data)
    cov_matrix = np.dot(transposed_data, data) / N
    return cov_matrix


def power_iteration(A, num_simulations=1000, tol=1e-6):
    b_k = np.random.rand(A.shape[1])
    for _ in range(num_simulations):
        b_k1 = np.dot(A, b_k)
        b_k1_norm = np.linalg.norm(b_k1)
        b_k = b_k1 / b_k1_norm
        if np.linalg.norm(np.dot(A, b_k) - b_k1_norm * b_k) < tol:
            break
    return b_k

def calculate_svd(C, k):
    eigenvectors = []
    for i in range(k):
        print(f"Calculating eigenvector {i+1}")
        eigenvector = power_iteration(C)
        eigenvectors.append(eigenvector)
        C = C - np.outer(eigenvector, eigenvector) * np.dot(eigenvector.T, np.dot(C, eigenvector))
    return np.array(eigenvectors).T


# Load images from the dataset folder
folder_path = r"src\backend\image\wifey"  # Replace with your dataset folder path
image_size = (100, 100)  # Replace with the desired consistent size
images = load_images_from_folder(folder_path, image_size)
print(f"Loaded {len(images)} images.")

# Calculate pixel averages
pixel_averages = calculate_pixel_averages(images)
print("Pixel averages calculated.")

# Standardize images
standardized_images = standardize_images(images, pixel_averages)
print("Images standardized.")

# Calculate covariance matrix
cov_matrix = hitung_kovarian(standardized_images)
print("Covariance matrix calculated.")

# Perform SVD manually and project the data onto the top k principal components
k = 10  # Replace with the desired number of principal components
Uk = calculate_svd(cov_matrix, k)
print("SVD calculated.")

# Project the data onto the top k principal components
Z = np.dot(standardized_images, Uk)
print("Data projected onto top principal components.")

# Print the projected data for verification
print(Z)