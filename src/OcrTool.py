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


    #def execute(self):