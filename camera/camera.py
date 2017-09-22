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
def frame_image(res_x, res_y, dist_to_target, size_of_target):
    # what percentage of the image does the target occupy?
    (u, v) = ( focal_length * size_of_target / dist_to_target ) / res_x , ( focal_length * size_of_target / dist_to_target ) / resolution_y
    print(u, v)
    return ((1 - u) / 2, (1 - v) / 2, u, v)

resolution_x = 2952
resolution_y = 1944

camera.resolution = (resolution_x, resolution_y)
camera.zoom = frame_image(resolution_x, resolution_y, DIST_FROM_LENSE_TO_GROUND, SIZE_OF_TARGET_ZONE)
camera.capture('../foo.jpg')