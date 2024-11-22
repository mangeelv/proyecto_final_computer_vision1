from picamera2 import Picamera2
import cv2
import os

def stream_video():
    # Inicializar Picamera2
    picam = Picamera2()
    
    # Configurar la resolución y formato de la cámara
    picam.preview_configuration.main.size = (1280, 720)  # Resolución
    picam.preview_configuration.main.format = "RGB888"  # Formato de color
    picam.preview_configuration.align()
    picam.configure("preview")
    picam.start()

    # Contador para las imágenes capturadas
    i = 0
    
    # Ruta para guardar las imágenes
    save_path = "../images/calib_images"
    os.makedirs(save_path, exist_ok=True)  # Asegurarse de que el directorio existe

    print("Presiona 'q' para capturar una imagen y salir.")

    while True:
        # Capturar el frame actual
        frame = picam.capture_array()

        # Mostrar el frame en una ventana
        cv2.imshow("PiCamera Video Stream", frame)

        # Detectar la tecla presionada
        if cv2.waitKey(1) & 0xFF == ord('q'):
            # Ruta completa del archivo de la imagen
            file_path = os.path.join(save_path, f"c_image{i}.jpg")
            
            # Guardar el frame actual
            cv2.imwrite(file_path, frame)
            print(f"Imagen guardada como: {file_path}")
            break  # Salir del bucle después de guardar la imagen
        
        i += 1

    # Liberar recursos
    cv2.destroyAllWindows()
    picam.stop()

# Llamar a la función
stream_video()
