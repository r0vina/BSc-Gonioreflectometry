# Remove the background using a mask (created using facebook's SegmentAnything) 
# Also read the GPS tags and convert them to solar Azimuth and Altitude.


import cv2 as cv
import glob
import itertools
import exifread
from astral import sun
from astral import LocationInfo
from datetime import datetime
import pytz

# Remove the rest of the image around the object using mask.
def binary_masking(image, mask):
    return cv.bitwise_and(image, image, mask=mask)

# Subtract environmental light
def env_color_removal(lit_image, unlit_image):
    return cv.subtract(lit_image, unlit_image)

def sorter(item):
    return item[-6:-4]

def sun_coordinates(filename):

    with open(filename, 'rb') as f:
        tags = exifread.process_file(f)
    gps_latitude = tags['GPS GPSLatitude'].values
    gps_longitude = tags['GPS GPSLongitude'].values
    gps_latituderef = tags['GPS GPSLatitudeRef'].values
    gps_longituderef = tags['GPS GPSLongitudeRef'].values
    datetime_photo = tags.get('EXIF DateTimeOriginal').values
    gps_altitude = tags['GPS GPSAltitude'].values
    gps_altituderef = tags['GPS GPSAltitudeRef'].values
    print(gps_latitude[0].num)
    # Convert to decimal degrees

    latitude = (gps_latitude[0].num / gps_latitude[0].den) + (gps_latitude[1].num / gps_latitude[1].den / 60) + (
                gps_latitude[2].num / gps_latitude[2].den / 3600)
    longitude = (gps_longitude[0].num / gps_longitude[0].den) + (gps_longitude[1].num / gps_longitude[1].den / 60) + (
                gps_longitude[2].num / gps_longitude[2].den / 3600)
    altitude = gps_altitude[0].num / gps_altitude[0].den

    timezone = pytz.timezone("Europe/Copenhagen")

    datetime_photo = datetime.strptime(datetime_photo, '%Y:%m:%d %H:%M:%S')

    dt_tz = timezone.localize(datetime_photo)
    print(dt_tz)

    print(gps_latituderef, latitude, longitude, datetime_photo, datetime.now(), gps_altitude)
    location = LocationInfo("Farum", "Denmark", "Europe/Copenhagen", latitude, longitude)
    location.observer.elevation = gps_altitude[0]
    print(location.observer)

    azimuth = sun.azimuth(location.observer, dateandtime=dt_tz)
    altitude = sun.elevation(location.observer, dateandtime=dt_tz)

    print(azimuth, altitude)

class ImageProcess:
    def __init__(self, lit_image_folder = None, unlit_image_folder = None, masks_folder =  None, results_path = None):
        self.lit_image_folder = lit_image_folder
        self.masks_folder = masks_folder
        self.unlit_image_folder = unlit_image_folder
        self.lit_images = None
        self.unlit_images = None
        self.masks = None
        self.results_path = results_path
        self.load_images()
        self.process()

    def process(self):
        for i in range(len(self.lit_images)):
            mask = cv.imread(self.masks[i], cv.IMREAD_GRAYSCALE)
            lit = binary_masking(cv.imread(self.lit_images[i]), mask)
            #sun_coordinates(self.lit_images[i])
            unlit = binary_masking(cv.imread(self.unlit_images[i]), mask)
            result = env_color_removal(lit, unlit)
            cv.imwrite(f"{self.results_path}/result{i+1}.jpg", result)


    def load_images(self):
        if self.lit_image_folder is not None:
            self.lit_images = self.get_filenames(self.lit_image_folder)
        if self.unlit_image_folder is not None:
            self.unlit_images = self.get_filenames(self.unlit_image_folder)
        if self.unlit_image_folder is not None:
            self.masks = self.get_filenames(self.masks_folder)

    def get_filenames(self, folder_name):
        exts = [f"{folder_name}/*.jpg",f"{folder_name}/*.png"]
        fnames = [glob.glob(ext) for ext in exts]
        fnames = sorted(itertools.chain.from_iterable(fnames), key=sorter)
        print(fnames)
        return fnames

impr = ImageProcess("imgs/lit", "imgs/unlit", "imgs/masks", "imgs/results")
print(impr.masks)

