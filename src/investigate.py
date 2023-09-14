import os
import cv2
from skimage.metrics import structural_similarity as compare_ssim

input_dir = "./uploads/OcrTool/Tesseract/Signatures"


def compare_images(image1, image2):
    return compare_ssim(image1, image2)


unmatch_siganature = {}

for folder_name in os.listdir(input_dir):
    std_id = folder_name
    print(f"checking signature for student {std_id}...\n")

    not_matching = {}

    similarity_threshold = 0.6
    student_folder = os.path.join(input_dir, folder_name)
    if os.path.isdir(student_folder):
        signature_files = os.listdir(student_folder)
        print(signature_files)
        if len(signature_files) >= 2:
            for i, current_signature in enumerate(signature_files):
                compre_list = signature_files[:i] + signature_files[i + 1 :]
                truth_score = 0
                image1 = cv2.imread(
                    os.path.join(student_folder, current_signature),
                    cv2.IMREAD_GRAYSCALE,
                )
                for j, nxt_signature in enumerate(compre_list):
                    image2 = cv2.imread(
                        os.path.join(student_folder, nxt_signature),
                        cv2.IMREAD_GRAYSCALE,
                    )
                    truth_score += compare_images(image1, image2)
                if truth_score / (len(signature_files) - 1) < similarity_threshold:
                    date = os.path.splitext(current_signature)[0]
                    print(f"student signature for {date} is not matching!")
                    not_matching[{std_id}] = date
