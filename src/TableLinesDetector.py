import cv2
from PIL import Image, ImageOps



class TableLinesDetector:
    def __init__(self, image):
        self.image = image

    # Read image - PIL Image
    def read_image(self):
        pass

    # Store processed image - PIL Image
    def store_process_image(self, output_path, image):
        image.save(output_path)

    # Convert image to grayscale - PIL Image
    def convert_image_to_grayscale(self):
        self.grayscale_image = ImageOps.grayscale(self.image)