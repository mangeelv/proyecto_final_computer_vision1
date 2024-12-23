# Obsoleto
import os
import cv2
import imageio
import numpy as np
from typing import List, Tuple
import glob
import shutil
import matplotlib.pyplot as plt
from skimage import filters, feature, io, color
import copy
from number_detector import *
from picamera2 import Picamera2
def get_picam2():
    picam2 = Picamera2()
    config = picam2.create_preview_configuration(
        main={"size": (640, 480), "format": "XRGB8888"},
    )
    picam2.configure(config)
    return picam2
def extract_number_from_image(green_mask: np.array, img: np.array) -> tuple[np.array, tuple[int, int, int, int]]:
    """
    Detecta el número en la imagen, recorta el área delimitada y devuelve la imagen recortada junto con las coordenadas.
    
    Args:
        green_mask (np.array): Máscara binaria de la región de interés.
        img (np.array): Imagen original.
    
    Returns:
        tuple: Imagen recortada y coordenadas (x, y, w, h) del contorno más grande.
    """
    # Encontrar los contornos en la máscara
    contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        # Encontrar el contorno más grande
        largest_contour = max(contours, key=cv2.contourArea)
        
        # Obtener la caja delimitadora (bounding box) del contorno más grande
        x, y, w, h = cv2.boundingRect(largest_contour)

        # Recortar la imagen usando la caja delimitadora
        cropped_img = img[y:y+h, x:x+w]
        cropped_img = cv2.resize(cropped_img, (200, 264), interpolation=cv2.INTER_LINEAR)
        
        return cropped_img, (x, y, w, h)
    else:
        # Si no se encuentra un contorno, devolver la imagen original y coordenadas vacías
        return img, None
if __name__ == "__main__":
    picam2 = get_picam2()
    picam2.start()
    tracking = False
    tracking_coords = None

    while True:
        img = picam2.capture_array()

        if tracking and tracking_coords:
            x, y, w, h = tracking_coords
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cropped_img = img[y:y + h, x:x + w]
            detected_number = detect_number(cropped_img)
            cv2.putText(img, f"Tracking: {detected_number}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        elif not tracking:
            cropped_img, coords = extract_number_from_image(color_segment(img)[0],img)
            if cropped_img is not None:
                detected_number = detect_number(cropped_img)
                cv2.putText(img, f"Detected: {detected_number}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow("frame", img)

        key = cv2.waitKey(1)
        if key == ord("q") and coords is not None:
            tracking = True
            tracking_coords = coords  # Guardar coordenadas de seguimiento
        elif key == 27:  # Escape para salir
            break

    picam2.stop()
    cv2.destroyAllWindows()