from PIL import Image


class TableExtractor:

    def __init__(self, image_path):
        self.image_path = image_path
        

    # Read image - PIL Image
    def read_image(self):
        self.image = Image.open(self.image_path)

    # Store processed image - PIL Image
    def store_process_image(self, output_path, image):
        image.save(output_path)

    

    def execute(self):
        self.read_image()
        self.store_process_image(
            "./uploads/0_original.jpg", self.image)
        