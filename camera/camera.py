from picamera import PiCamera
from detector import filter_green
import numpy as np
import time

DIST_FROM_LENSE_TO_GROUND = 39.5
SIZE_OF_TARGET_ZONE = 10
CAMERA_MODULE = "v1.3"

# All measurements in millimeters
RESOLUTION_X = 1920
RESOLUTION_Y = 1080
PIXEL_WIDTH = .0014
FOCAL_LENGTH = 3.60

sensor_width = PIXEL_WIDTH * RESOLUTION_X
sensor_height = PIXEL_WIDTH * RESOLUTION_Y

# dist_to_target - distance between lens and target (in mm)
# size_of_target - one side of
# returns: 4-tuple of (x, y, w, h)
def frame_image(sensor_width, sensor_height, dist_to_target, size_of_target):
    # what percentage of the image does the target occupy?
    (u, v) = ( focal_length * size_of_target / dist_to_target ) / sensor_width , ( focal_length * size_of_target / dist_to_target ) / sensor_height
    return ((1 - u) / 2, (1 - v) / 2, u, v)

def square_has_plant():
    with picamera.PiCamera() as camera:
        camera.resolution(RESOLUTION_X, RESOLUTION_Y)
        camera.zoom = frame_image(sensor_width, sensor_height, DIST_FROM_LENSE_TO_GROUND, SIZE_OF_TARGET_ZONE)
        time.sleep(2)
        image = np.empty((RESOLUTION_Y * RESOLUTION_X * 3,), dtype=np.uint8)
        camera.capture(image, 'bgr')
        return filter_green(image)
