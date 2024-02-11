import base64
import numpy as np
import cv2
from time import time
import openai_hack

class Camera():

    def get_photo(self):
        rv, image = self.camera_capture.read()
        _, im_arr = cv2.imencode('.png', image)
        im_bytes = im_arr.tobytes()
        im_b64 = base64.b64encode(im_bytes)
        self.camera_capture.release()
        cv2.imwrite(f'image_{time()}.png', image)
        return im_b64

    def __init__(self):
        self.camera_capture = cv2.VideoCapture(0)

    def to_base_64(self, image_data):
        start_time = time.time

        # Path to your image
        image_path = f"image{start_time}.jpg"

        # Getting the base64 string
        base64_image = base64.b64encode(image_data).decode('utf-8')

        return base64_image

camera = Camera()
openai_hack.image_description(camera.get_photo().decode('utf-8'))

