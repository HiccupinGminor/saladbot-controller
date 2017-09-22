from picamera import PiCamera
camera = PiCamera()

DIST_FROM_LENSE_TO_GROUND = 39.5
SIZE_OF_TARGET_ZONE = 10
CAMERA_MODULE = "v1.3"

if CAMERA_MODULE is "v1.3":
    sensor_width = 3.76
    sensor_height = 2.74
    focal_length = 3.60 # millimeters

# dist_to_target - distance between lens and target (in mm)
# size_of_target - one side of
# returns: 4-tuple of (x, y, w, h)
def frame_image(sensor_width, sensor_height, dist_to_target, size_of_target):
    # what percentage of the image does the target occupy?
    (u, v) = ( focal_length * size_of_target / dist_to_target ) / sensor_width , ( focal_length * size_of_target / dist_to_target ) / sensor_height
    print(u, v)
    return ((1 - u) / 2, (1 - v) / 2, u, v)

resolution_x = 1920
resolution_y = 1080

camera.resolution = (resolution_x, resolution_y)
camera.zoom = frame_image(sensor_width, sensor_height, DIST_FROM_LENSE_TO_GROUND, SIZE_OF_TARGET_ZONE)
camera.capture('../foo.jpg')