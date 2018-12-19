import cv2
import requests
import numpy as np
import os

DIFFERENT = 0
SAME = 1
FACES_NOT_FOUND = 2

def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

# gets url of an image and returns the image as ndarray
def get_image_from_URL(image_url):
    response = requests.get(image_url)
    coded_image = response.content

    decoded = cv2.imdecode(np.frombuffer(coded_image, np.uint8), -1)
    image = cv2.cvtColor(decoded, cv2.COLOR_BGR2RGB)
    return image


import face_recognition




# gets 2 images of humans and returns if they are the same person
def compare_between_faces(image1, image2, tolerance=0.6):

    try:
        image1_encodings = face_recognition.face_encodings(image1)
        image2_encodings = face_recognition.face_encodings(image2)
    except IndexError:
        print("faces were not found")
        return FACES_NOT_FOUND
        quit()
    results = False
    for image1_encoding in image1_encodings:
        for image2_encoding in image2_encodings:
            results = face_recognition.compare_faces([image1_encoding], image2_encoding, tolerance)[0] or results
    if results:
        return SAME
    return DIFFERENT

