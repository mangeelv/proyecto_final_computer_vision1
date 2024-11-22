#################IMPORTAMOS LAS LIBRERIAS##########################
from typing import List
import numpy as np
import imageio
import cv2
import copy
import glob
import warnings
import matplotlib.pyplot as plt
import os 

warnings.filterwarnings("ignore")

#CREAMOS LAS FUNCIONES BASE QUE PODEMOS USAR: 
def load_images(filenames: List) -> List:
    return [imageio.imread(filename) for filename in filenames]
def show_image(img: np.array, img_name: str="Image"):
    cv2.imshow(img_name,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
def write_image(output_folder: str, img_name: str, img: np.array):
    img_path = os.path.join(output_folder,img_name)
    cv2.imwrite(img_path,img)


#COMENZAMOS CON EL PROCESO DE CALIBRACION DE LA CAMARA: 
