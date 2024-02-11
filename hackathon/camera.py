from dotenv import load_dotenv
import base64
import numpy as np
import cv2
from time import time
import socket
import os
import threading

load_dotenv()

HOST = os.getenv("CAMERA_HOST")
PORT = int(os.getenv("CAMERA_PORT"))

class Camera():

    def export_to_server(self, photo):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((HOST, PORT))
            self.socket.sendall(photo)
            self.socket.close()
        except:
            print(f"Error sending photo to {HOST}:{PORT}")

    def get_photo(self):
        camera_capture = cv2.VideoCapture(0)
        rv, image = camera_capture.read()
        _, im_arr = cv2.imencode('.png', image)
        im_bytes = im_arr.tobytes()
        im_b64 = base64.b64encode(im_bytes)
        camera_capture.release()
        cv2.imwrite(f'image_{time()}.png', image)
        self.export_to_server(im_b64)
        camera_capture.release()
        return im_b64

    def to_base_64(self, image_data):
        start_time = time.time

        # Path to your image
        image_path = f"image{start_time}.jpg"

        # Getting the base64 string
        base64_image = base64.b64encode(image_data).decode('utf-8')

        return base64_image

camera = Camera()


# openai.image_description(photo.decode('utf-8'))







# openai_hack.image_description(camera.get_photo().decode('utf-8'))

