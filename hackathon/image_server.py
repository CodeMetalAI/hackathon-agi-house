from dotenv import load_dotenv
import socket
import os

load_dotenv()

HOST = os.getenv("CAMERA_HOST")
PORT = int(os.getenv("CAMERA_PORT"))

import os
images_folder = "frames"
if not os.path.exists(images_folder):
    os.makedirs(images_folder)

from time import time
import base64
while 1:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            base64_image = b''
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(socket.MSG_WAITALL)
                if not data:
                    break
                base64_image += data

            decoded_base64_image = base64_image.decode('utf-8')
            with open(f"{images_folder}/out{time()}.png", "wb") as fh:
                fh.write(base64.decodebytes(base64_image))