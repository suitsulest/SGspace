import time
import picamera
import datetime
from orbit import *

"""This porogram just takes the pictures from the ISS.
    We will use the NDVI filter for the camera.
    Images info(lat, long) is stored as EXIF tags on the images.
    We will process the images on the ground. """
'''Camera will take a pic every minute until the time is 2h 58min after starting the porgram'''

def convert(angle):
    sign, degrees, minutes, seconds = angle.signed_dms()
    exif_angle = f'{degrees:.0f}/1,{minutes:.0f}/1,{seconds*10:.0f}/10'
    return sign < 0, exif_angle

camera = picamera.PiCamera()
duration = datetime.timedelta(hours=2,minutes=58)
interval = 60
start_time = datetime.datetime.now()
end_time = start_time + duration
i = 0
while datetime.datetime.now() < end_time:
    exif_latitude = convert(ISS.coordinates().latitude)[1]
    exif_longitude = convert(ISS.coordinates().longitude)[1]
    camera.exif_tags['latitude'] = exif_latitude
    camera.exif_tags['longitude'] = exif_longitude
    camera.capture(output=f'image{i}',resize=(3840, 2160), format='raw')
    time.sleep(interval)
    i += 1