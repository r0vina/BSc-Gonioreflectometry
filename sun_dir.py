import exifread
from astral import sun
from astral import LocationInfo
from datetime import datetime
import pytz
with open('../bsc/bunny125/light/lit011.jpg', 'rb') as f:
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

latitude = (gps_latitude[0].num/gps_latitude[0].den) + (gps_latitude[1].num/gps_latitude[1].den/60) + (gps_latitude[2].num/gps_latitude[2].den/3600)
longitude = (gps_longitude[0].num/gps_longitude[0].den) + (gps_longitude[1].num/gps_longitude[1].den/60) + (gps_longitude[2].num/gps_longitude[2].den/3600)
altitude = gps_altitude[0].num / gps_altitude[0].den

timezone = pytz.timezone("Europe/Copenhagen")

datetime_photo = datetime.strptime(datetime_photo, '%Y:%m:%d %H:%M:%S')

dt_tz = timezone.localize(datetime_photo)
print(dt_tz)

print(gps_latituderef, latitude,longitude, datetime_photo, datetime.now(), gps_altitude)
location = LocationInfo("Farum", "Denmark", "Europe/Copenhagen", latitude, longitude)
location.observer.elevation = gps_altitude[0]
print(location.observer)

azimuth = sun.azimuth(location.observer, dateandtime = dt_tz)
altitude = sun.elevation(location.observer, dateandtime = dt_tz)

print(azimuth,altitude)

import math

def convert_az_alt_to_xyz(observer_latitude, observer_longitude, azimuth, altitude):
    # Convert observer's latitude and longitude to geocentric coordinates
    observer_latitude_rad = math.radians(observer_latitude)
    observer_longitude_rad = math.radians(observer_longitude)
    X = math.cos(observer_latitude_rad) * math.cos(observer_longitude_rad)*100000000.0
    Y = math.cos(observer_latitude_rad) * math.sin(observer_longitude_rad)*100000000.0
    Z = math.sin(observer_latitude_rad)*100000000.0

    # Convert azimuth and altitude to spherical coordinates
    azimuth_rad = math.radians(azimuth)
    altitude_rad = math.radians(altitude)

    # Calculate direction vector of the sun in the observer's local coordinate system
    x = math.cos(azimuth_rad) * math.cos(altitude_rad)
    y = math.sin(azimuth_rad) * math.cos(altitude_rad)
    z = math.sin(altitude_rad)

    # Combine observer's geocentric coordinates with the direction vector of the sun
    X_s = X + x
    Y_s = Y + y
    Z_s = Z + z

    return X_s, Y_s, Z_s

# Example usage
observer_latitude = latitude  # Latitude of observer (e.g., London)
observer_longitude = longitude  # Longitude of observer (e.g., London)
#azimuth = 180  # Azimuth angle of the sun (degrees)
#altitude = 30  # Altitude angle of the sun (degrees)

X_s, Y_s, Z_s = convert_az_alt_to_xyz(observer_latitude, observer_longitude, azimuth, altitude)
print(f"Sun's XYZ coordinates: X = {X_s}, Y = {Y_s}, Z = {Z_s}")
