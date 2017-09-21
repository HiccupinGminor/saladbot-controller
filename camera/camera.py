from picamera import PiCamera
camera = PiCamera()

DIST_FROM_LENSE_TO_GROUND = 39.5
SIZE_OF_TARGET_ZONE = 10

# dist_to_target - distance between lens and target (in mm)
# size_of_target - one side of
def frame_image(dist_to_target,size_of_target):
    return (0.4, 0.4, 0.2, 0.2)

resolution_x = 1024
resolution_y = 768

camera.resolution = (resolution_x, resolution_y)
camera.zoom = frame_image(DIST_FROM_LENSE_TO_GROUND, SIZE_OF_TARGET_ZONE)
camera.capture()
