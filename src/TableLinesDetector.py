import cv2
from PIL import Image, ImageOps
from skimage.morphology import rectangle, binary_erosion, binary_dilation
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
 
    # Extracting vertical lines - skimage
    # erosion vertical lines
    def v_erosion_image(self, iterations):
        image_array = np.array(self.inverted_image)
        vertical_kernel = rectangle(10, 1)
        eroded_image_array = image_array.copy()  # Make a copy to preserve original
        for _ in range(iterations):
            eroded_image_array = binary_erosion(
                eroded_image_array, vertical_kernel)
        eroded_image_array = binary_erosion(
            eroded_image_array, rectangle(6, 6))
        self.v_eroded_image = Image.fromarray(eroded_image_array)

    # dilation vertical lines - skimage
    def v_dilation_image(self, iterations):
        image_array = np.array(self.v_eroded_image)
        vertical_kernel = rectangle(25, 1)
        dilated_image_array = image_array.copy()  # Make a copy to preserve original
        for _ in range(iterations):
            dilated_image_array = binary_dilation(
                dilated_image_array, vertical_kernel)
        self.v_dilated_image = Image.fromarray(dilated_image_array)

    # extracting horizontal lines
    # erosion horizontal lines - skimage
    def h_erosion_image(self, iterations):
        image_array = np.array(self.inverted_image)
        horizontal_kernel = rectangle(1, 10)
        eroded_image_array = image_array.copy()  # Make a copy to preserve original
        for _ in range(iterations):
            eroded_image_array = binary_erosion(
                eroded_image_array, horizontal_kernel)
        eroded_image_array = binary_erosion(
                eroded_image_array, rectangle(6, 6))
        self.h_eroded_image = Image.fromarray(eroded_image_array)

    # dilation horizontal lines - skimage
    def h_dilation_image(self, iterations):
        image_array = np.array(self.h_eroded_image)
        horizontal_kernel = rectangle(1, 17)
        dilated_image_array = image_array.copy()  # Make a copy to preserve original
        for _ in range(iterations):
            dilated_image_array = binary_dilation(
                dilated_image_array, horizontal_kernel)
        self.h_dilated_image = Image.fromarray(dilated_image_array)

    
    # Blending vertical and horizontal lines
    def blend_images(self, weight1, weight2, gamma=0.0):
        v_dilated_image_array = np.array(self.v_dilated_image)
        h_dilated_image_array = np.array(self.h_dilated_image)
        # numpy array used for blending (calculate on image data)
        blended_array = (weight1 * v_dilated_image_array +
                         weight2 * h_dilated_image_array + gamma).astype(np.uint8)

        # Normalize the blended array to [0, 255]
        blended_array = ((blended_array - blended_array.min()) /
                         (blended_array.max() - blended_array.min()) * 255).astype(np.uint8)
        # PIL image used for visualization(convert np to PIL)
        self.blended_image = Image.fromarray(blended_array)
    
    def threshold_blended_image(self):
        threshold_value = 120  # Adjust the threshold value as needed
        self.thresholded_blended_image = self.blended_image.point(
            lambda p: 255 if p > threshold_value else 0)
        
    def dilate_combined_image_to_make_lines_thicker(self):
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        img_array = np.array(self.thresholded_blended_image)
        self.combined_image_dilated = cv2.dilate(
            img_array, kernel, iterations=6)
        self.combined_image_dilated = Image.fromarray(
            self.combined_image_dilated)

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
        self.v_erosion_image(iterations=12)
        self.store_process_image(
            "./uploads/TableLinesDetector/20_vertical_eroded.jpg", self.v_eroded_image)
        self.v_dilation_image(iterations=10)
        self.store_process_image(
            "./uploads/TableLinesDetector/21_vertical_dilated.jpg", self.v_dilated_image)
        self.h_erosion_image(iterations=12)
        self.store_process_image(
            "./uploads/TableLinesDetector/22_horizontal_eroded.jpg", self.h_eroded_image)
        self.h_dilation_image(iterations=10)
        self.store_process_image(
            "./uploads/TableLinesDetector/23_horizontal_dilated.jpg", self.h_dilated_image)
        self.blend_images(1, 1)
        self.store_process_image(
            "./uploads/TableLinesDetector/24_blended.jpg", self.blended_image)
        self.threshold_blended_image()
        self.store_process_image(
            "./uploads/TableLinesDetector/25_thresholded_blended_image.jpg", self.thresholded_blended_image)
        self.dilate_combined_image_to_make_lines_thicker()
        self.store_process_image(
            "./uploads/TableLinesDetector/26_dilated_combined_image.jpg", self.combined_image_dilated)
        return self.thresholded_blended_image
        