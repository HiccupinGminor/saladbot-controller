from picamera import PiCamera
from detector import filter_green
import numpy as np
import time

DIST_FROM_LENSE_TO_GROUND = 39.5
SIZE_OF_TARGET_ZONE = 10
CAMERA_MODULE = "v1.3"

resolution_x = 1920
resolution_y = 1080
pixel_width = .0014

# All measurements in millimeters
if CAMERA_MODULE is "v1.3":
    focal_length = 3.60

sensor_width = pixel_width * resolution_x
sensor_height = pixel_width * resolution_y

# dist_to_target - distance between lens and target (in mm)
# size_of_target - one side of
# returns: 4-tuple of (x, y, w, h)
def frame_image(sensor_width, sensor_height, dist_to_target, size_of_target):
    # what percentage of the image does the target occupy?
    (u, v) = ( focal_length * size_of_target / dist_to_target ) / sensor_width , ( focal_length * size_of_target / dist_to_target ) / sensor_height
    return ((1 - u) / 2, (1 - v) / 2, u, v)

def square_has_plant():
    with picamera.PiCamera() as camera:
        camera.resolution(resolution_x, resolution_y)
        camera.zoom = frame_image(sensor_width, sensor_height, DIST_FROM_LENSE_TO_GROUND, SIZE_OF_TARGET_ZONE)
        time.sleep(2)
        image = np.empty((resolution_y * resolution_x * 3,), dtype=np.uint8)
        camera.capture(image, 'bgr')
        return filter_green(image)
