from PIL import Image
import os
import numpy as np
import matplotlib.pyplot as plt
#import kagglehub

# First Step: Image Processing and Loading
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
    old_height, old_width = len(image_matrix), len(image_matrix[0])
    resized_matrix = [[0 for _ in range(new_width)] for _ in range(new_height)]
    
    for i in range(new_height):
        for j in range(new_width):
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
            images.append((img, resized_matrix))
    return images
# Step Two: Data Centering (Standardization)
def calculate_pixel_averages(images):
    width, height = len(images[0][1][0]), len(images[0][1])
    N = len(images)
    pixel_sums = [[0 for _ in range(width)] for _ in range(height)]
    
    for _, img in images:
        for i in range(height):
            for j in range(width):
                pixel_sums[i][j] += img[i][j]
    
    pixel_averages = [[pixel_sums[i][j] / N for j in range(width)] for i in range(height)]
    return pixel_averages

def standardize_images(images, pixel_averages):
    standardized_images = []
    for _, img in images:
        width, height = len(img[0]), len(img)
        standardized_matrix = [[0 for _ in range(width)] for _ in range(height)]
        
        for i in range(height):
            for j in range(width):
                standardized_matrix[i][j] = img[i][j] - pixel_averages[i][j]
        
        standardized_images.append(grayscale_to_1d_vector(standardized_matrix))
    return standardized_images

# Step Three: PCA Computation Using Singular Value Decomposition (SVD)
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

def calculate_eigendecomposition(C):
    n = len(C)
    eigenvalues = np.zeros(n)
    eigenvectors = np.zeros((n, n))
    
    C_remaining = np.array(C)
    
    for i in range(10):
        print(f"Calculating eigenvector {i+1}")
        v = np.random.rand(n)
        v = v / np.linalg.norm(v)
        
        for _ in range(100):
            Cv = np.dot(C_remaining, v)
            lambda_i = np.dot(v, Cv) / np.dot(v, v)
            
            v_new = Cv / np.linalg.norm(Cv)
            
            if np.allclose(v, v_new, rtol=1e-6):
                break
            v = v_new
            
        eigenvalues[i] = lambda_i
        eigenvectors[:, i] = v
        
        C_remaining = C_remaining - lambda_i * np.outer(v, v)
    
    idx = eigenvalues.argsort()[::-1]
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]
    
    return eigenvectors, eigenvalues

def calculate_svd(C, k):
    U, S = calculate_eigendecomposition(C)
    Uk = U[:, :k]
    Sk = np.diag(S[:k])
    
    return Uk

def project_query_image(query_image_path, pixel_averages, Uk, image_size):
    img = Image.open(query_image_path)
    grayscale_matrix = rgbToGrayscale(img)
    resized_matrix = resize_image_manual(grayscale_matrix, image_size[0], image_size[1])
    standardized_matrix = [[resized_matrix[i][j] - pixel_averages[i][j] for j in range(image_size[0])] for i in range(image_size[1])]
    standardized_vector = grayscale_to_1d_vector(standardized_matrix)
    q = np.dot(standardized_vector, Uk)
    return img, q

def calculate_euclidean_distances(query_vector, projected_data):
    distances = []
    for i, z in enumerate(projected_data):
        distance = np.linalg.norm(query_vector - z)
        distances.append((i, distance))
    return distances

def sort_by_distance(distances):
    return sorted(distances, key=lambda x: x[1])

# Main execution
folder_path = r"src\backend\image\testing"
image_size = (64, 64)
images = load_images_from_folder(folder_path, image_size)
print(f"Loaded {len(images)} images.")

pixel_averages = calculate_pixel_averages(images)
print("Pixel averages calculated.")

standardized_images = standardize_images(images, pixel_averages)
print("Images standardized.")

cov_matrix = hitung_kovarian(standardized_images)
print("Covariance matrix calculated.")

k = 10  # Number of principal components to retain
Uk = calculate_svd(cov_matrix, k)
print("SVD calculated.")

# Project data onto principal components
Z = np.dot(standardized_images, Uk)
print("Data projected onto principal components.")

# Process query image
query_image_path = r"src\backend\image\tomoyotes.jpg"
query_img, q = project_query_image(query_image_path, pixel_averages, Uk, image_size)
print("Query image projected.")

# Calculate similarities
distances = calculate_euclidean_distances(q, Z)
sorted_distances = sort_by_distance(distances)
print("Distances calculated and sorted.")

# Find similar images
threshold_distance = np.percentile([d for _, d in sorted_distances], 20)
similar_images_indices = [i for i, d in sorted_distances if d <= threshold_distance]

# Visualize results
fig, axs = plt.subplots(1, len(similar_images_indices) + 1, figsize=(15, 6))
axs[0].imshow(query_img)
axs[0].set_title('Query Image')
axs[0].axis('off')

for idx, image_index in enumerate(similar_images_indices):
    similar_image = images[image_index][0]
    axs[idx + 1].imshow(similar_image)
    axs[idx + 1].set_title(f'Similar Album {idx + 1}')
    axs[idx + 1].axis('off')

plt.show()