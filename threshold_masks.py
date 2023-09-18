import os
import cv2
import numpy as np
from PIL import Image

def remove_noise_and_threshold_masks(folder_path):
    # Iterate through the files in the folder
    for file_name in os.listdir(folder_path):
        mask_image = Image.open(folder_path+file_name)
        mask_image = mask_image.convert("L")

        threshold = 128
        binary_mask = np.array(mask_image) > threshold

        binary_mask_image = Image.fromarray(binary_mask.astype(np.uint8) * 255)
        binary_mask_image.save(f"{folder_path}thresholded_{file_name}")
# Specify the folder path containing the masks
folder_path = "/home/roneetnagale/DTU_OneDrive/DTU/bsc/bunny125/light/masks/"

# Call the function to remove noise and perform thresholding
remove_noise_and_threshold_masks(folder_path)
