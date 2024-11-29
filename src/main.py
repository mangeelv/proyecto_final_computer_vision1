from picamera2 import Picamera2
import cv2
import os
import threading
import number_detector as nd

picam = Picamera2()
picam.preview_configuration.main.size=(320, 180) # Esto es la resolución, se puede dividir entre 2
picam.preview_configuration.main.format="RGB888"
picam.preview_configuration.align()
picam.configure("preview")
picam.start()


def stream_video():
    while True:
        frame = picam.capture_array()
        cv2.imshow("picam", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()


def photo_taker():
    while True:
        entrada = input("Presiona Enter para hacer una detección...")
        if entrada == "":
            picam.start_and_capture_file("../images/temp.jpg")
            nd.make_detection()
        
if __name__ == "__main__":

    try:
        photo_taker_thread = threading.Thread(target=photo_taker, daemon=True)  # Daemon=True para finalizar automáticamente con el programa
        stream_thread = threading.Thread(target=stream_video, daemon=True)  # Daemon=True para finalizar automáticamente con el programa
        photo_taker_thread.start()
        stream_thread.start()
        photo_taker_thread.join()
        stream_thread.join()
    except KeyboardInterrupt:
        pass
    
