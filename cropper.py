import matplotlib.pyplot as plt
import cv2 as cv

from bg_deletion import ImageProcess

impr = ImageProcess("../bsc/checker/", results_path="../bsc/checker/cropped")
print(impr.lit_image_folder)
def cropper(img):
    # Get the dimensions of the image
    height, width = img.shape[:2]

    # Calculate the center coordinates of the image
    center_x =  int(width / 2)
    center_y = int(height / 2)

    # Set the size of the square to be cropped
    crop_size = 2000

    # Calculate the coordinates of the top-left corner of the crop
    crop_x = int(center_x - (crop_size / 2))
    crop_y = int(center_y - (crop_size / 2))

    # Crop the image
    cropped_img = img[crop_y:crop_y + crop_size, crop_x:crop_x + crop_size]

    # Display the original and cropped images
    #cv.imshow('Original Image', img)
    #cv.imshow('Cropped Image', cropped_img)
    return cropped_img

i = 0
for image_path in impr.lit_images:

    image = cv.imread(image_path)
    cropped_image = cropper(image)
    cv.imwrite(f"{impr.results_path}/check{i+1}.jpg", cropped_image)
    #cv.waitKey(0)
    print(i)
    i+=1
i=0

for image_path in impr.unlit_images:

    image = cv.imread(image_path)
    cropped_image = cropper(image)
    cv.imwrite(f"{impr.results_path}/shade/unlit{i+1}.jpg", cropped_image)
    #cv.waitKey(0)
    print(i)
    i+=1
i=0


print(impr.lit_images)