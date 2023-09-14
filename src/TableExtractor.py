from PIL import Image, ImageOps



class TableExtractor:

    def __init__(self, image_path):
        self.image_path = image_path
        self.rectangular_contours = []

    # Read image - PIL Image
    def read_image(self):
        self.image = Image.open(self.image_path)

    # Store processed image - PIL Image
    def store_process_image(self, output_path, image):
        image.save(output_path)

    # Convert image to grayscale - PIL Image
    def convert_image_to_grayscale(self):
        self.grayscale_image = ImageOps.grayscale(self.image)

    def denoise_image(self):
        kernal = gf.gaussian_kernel(5, 1)
        self.denoised_image = gf.gaussian_filter(self.grayscale_image, kernal)

    # Threshold image - PIL Image
    def threshold_image(self):
        self.thresholded_image = Image.fromarray(gt.apply_adaptive_threshold_gaussian(self.denoised_image, 27, 10, 5))

    # Invert image - PIL Image
    def invert_image(self):
        self.inverted_image = ImageOps.invert(self.thresholded_image)

    # Extracting vertical lines - skimage
    # erosion vertical lines
    def v_erosion_image(self, iterations=1):
        # Convert PIL Image to NumPy array
        image_array = np.array(self.inverted_image)
        # Create a vertical erosion kernel
        vertical_kernel = rectangle(5, 1)
        # Perform vertical erosion iteratively on the image array
        eroded_image_array = image_array.copy()  # Make a copy to preserve original
        for _ in range(iterations):
            eroded_image_array = binary_erosion(
                eroded_image_array, vertical_kernel)
        # Convert the eroded image array back to PIL Image
        self.v_eroded_image = Image.fromarray(eroded_image_array)



    def execute(self):
        self.read_image()
        self.store_process_image(
            "./uploads/TableExtractor/0_original.jpg", self.image)
        self.convert_image_to_grayscale()
        self.store_process_image(
            "./uploads/TableExtractor/1_grayscaled.jpg", self.grayscale_image)
        self.denoise_image()
        self.threshold_image()
        self.store_process_image(
            "./uploads/TableExtractor/2_thresholded.jpg", self.thresholded_image)
        self.invert_image()
        self.store_process_image(
            "./uploads/TableExtractor/3_inverteded.jpg", self.inverted_image)
        self.v_erosion_image(iterations=5)
        self.store_process_image(
            "./uploads/TableExtractor/4_vertical_eroded.jpg", self.v_eroded_image)
        