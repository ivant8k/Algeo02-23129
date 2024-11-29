from PIL import Image
import os

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

# tes drive
folder_path =  r"src\backend\image\wifey" 
image_size = (100, 100)
images = load_images_from_folder(folder_path, image_size)

pixel_averages = calculate_pixel_averages(images)


standardized_images = standardize_images(images, pixel_averages)

print(standardized_images[0])