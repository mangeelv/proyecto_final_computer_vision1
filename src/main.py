from picamera2 import Picamera2
import cv2
import os
import threading

picam = Picamera2()
picam.preview_configuration.main.size=(640, 360) # Esto es la resolución, se puede dividir entre 2
picam.preview_configuration.main.format="RGB888"
picam.preview_configuration.align()
picam.configure("preview")
picam.start()


def photo_taker():
    while True:
        entrada = input("Presiona Enter para hacer una detección...")
        if entrada == "":
            picam.start_and_capture_file("../images/temp.jpg")
        
if __name__ == "__main__":

    try:
        photo_taker_thread = threading.Thread(target=photo_taker, daemon=True)  # Daemon=True para finalizar automáticamente con el programa
        photo_taker_thread.start()
        photo_taker_thread.join()
    except KeyboardInterrupt:
        pass
    
