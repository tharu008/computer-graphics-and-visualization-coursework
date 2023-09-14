import cv2
from PIL import Image, ImageOps
import numpy as np
import gaussian_filter as gf
import gaussian_thresholding as gt



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
    
    def denoise_image(self):
        kernal = gf.gaussian_kernel(5, 2)
        self.denoised_image = gf.gaussian_filter(self.grayscale_image, kernal)

    # Threshold image - PIL Image
    def threshold_image(self):
        self.thresholded_image = Image.fromarray(gt.apply_adaptive_threshold_gaussian(self.denoised_image, 27, 10, 5))
        # threshold_value = 150  # Adjust the threshold value as needed
        # self.thresholded_image = self.grayscale_image.point(
        #     lambda p: 255 if p > threshold_value else 0)

    # Invert image - PIL Image
    def invert_image(self):
        self.inverted_image = ImageOps.invert(self.thresholded_image)
 
 

    def execute(self):
        self.read_image()
        self.store_process_image(
            "./uploads/TableLinesDetector/16_original_img_with_padding.jpg", self.image)
        self.convert_image_to_grayscale()
        self.store_process_image(
            "./uploads/TableLinesDetector/17_grayscaled.jpg", self.grayscale_image)
        self.denoise_image()
        self.threshold_image()
        self.store_process_image(
            "./uploads/TableLinesDetector/18_thresholded.jpg", self.thresholded_image)
        self.invert_image()
        self.store_process_image(
            "./uploads/TableLinesDetector/19_inverteded.jpg", self.inverted_image)