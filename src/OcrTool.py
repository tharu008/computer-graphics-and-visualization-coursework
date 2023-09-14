import cv2
import numpy as np


class OcrTool:
    def __init__(self, image_with_lines_detected, perspective_corrected_image, xml_file_path, image_path):
        self.binarized_img = image_with_lines_detected
        self.image = perspective_corrected_image
        self.xml_path = xml_file_path
        self.image_path = f"{image_path}"

    # Store processed image - PIL Image
    def store_process_image(self, output_path, image):
        image.save(output_path)

    def dilate_image(self):
        kernel_to_remove_gaps_between_words = np.array([
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1]
        ])
        img_array = np.array(self.binarized_img)
        self.dilated_image = cv2.dilate(
            img_array, kernel_to_remove_gaps_between_words, iterations=1)
        simple_kernel = np.ones((3, 3), np.uint8)
        self.dilated_image = cv2.dilate(
            self.dilated_image, simple_kernel, iterations=1)
        self.dilated_image = Image.fromarray(self.dilated_image)
    
    def execute(self):
        self.dilate_image()
        self.store_process_image(
           './uploads/OcrTool/28_dilated_image.jpg', self.dilated_image)
        