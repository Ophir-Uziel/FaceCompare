import cv2
import requests
import numpy as np
from matplotlib.pyplot import *

def main(image_url):
    image_new_url = "https://scontent.flhr5-1.fna.fbcdn.net/v/t34.0-12/16176889_112685309244626_578204711_n.jpg?_nc_cat=1&_nc_ht=scontent.flhr5-1.fna&oh=856c61f91aeb1966e31151651d9d22dc&oe=5C0FED68"
    response = requests.get(image_new_url)
    image = response.content

    decoded = cv2.imdecode(np.frombuffer(image, np.uint8), -1)
    decoded = cv2.cvtColor(decoded, cv2.COLOR_RGB2BGR)
    imshow(decoded)
    show()
    print('OpenCV:\n', decoded)
    print(type(image))
    print(str(image))


main("")



# gets url of an image and returns the image as ndarray
def get_image_from_URL(image_url):
    response = requests.get(image_url)
    coded_image = response.content

    decoded = cv2.imdecode(np.frombuffer(coded_image, np.uint8), -1)
    image = cv2.cvtColor(decoded, cv2.COLOR_BGR2RGB)
    return image