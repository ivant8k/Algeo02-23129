from PIL import Image
import math

def rgbToGrayscale(RGBImage):
    width, height = RGBImage.size

    matrix = [[0 for i in range (width)] for j in range (height)]
    
    for i in range(height):
        for j in range(width):
            r, g, b = RGBImage.getpixel((j, i))
            gscalevalue = int(0.2989 * r + 0.587 * g + 0.114 * b)
            matrix[i][j] = gscalevalue
    
    return matrix

