from picamera2 import Picamera2
import cv2
import threading
import number_detector as nd

picam = Picamera2()
picam.preview_configuration.main.size=(264, 264) # Esto es la resolución, se puede dividir entre 2
picam.preview_configuration.main.format="RGB888"
picam.preview_configuration.align()
picam.configure("preview")
picam.start()

detected = 0 # variable que guarda el valor del numero detectado
def stream_video():
    '''Hilo encargado de hacer el streaming del video, mostrando por pantalla el tracker del numero 
    a partir de las coordenadas de extract_number_from_image y mostrando también el número detectado'''
    global detected
    color = (0, 255, 0)  
    thickness = 2 
    while True:
        frame = picam.capture_array()
        frame = cv2.resize(frame, (264,264), interpolation=cv2.INTER_LINEAR)
        if nd.track_window != None:      
            x, y, w, h = nd.track_window
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, thickness)
        cv2.putText(frame, f"Detected: {detected}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.imshow("picam", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()


def photo_taker():
    ''''Hilo que se encagra de tomar fotos y guardarlas, para hacer detecciones'''
    while True:
        global detected
        picam.capture_file("../images/temp.jpg")
        detected = nd.make_detection()
       
   
        
if __name__ == "__main__":

    try:
        photo_taker_thread = threading.Thread(target=photo_taker, daemon=True)  # Daemon=True para finalizar automáticamente con el programa
        stream_thread = threading.Thread(target=stream_video, daemon=True) 
        photo_taker_thread.start()
        stream_thread.start()
        photo_taker_thread.join()
        stream_thread.join()
    except KeyboardInterrupt:
        pass
    
