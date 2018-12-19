import cv2
def resize(image, max_height, max_width):
    current_size = image.size()
    factor = min(max_height/current_size[0], max_width/current_size[1])
    return cv2.resize(image, (0,0), factor, factor, cv2.INTER_AREA)