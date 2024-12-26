from picamera2 import Picamera2
import cv2
import threading
import number_detector as nd
import time

picam = Picamera2()
picam.preview_configuration.main.size=(264, 264) # Esto es la resolución, se puede dividir entre 2
picam.preview_configuration.main.format="RGB888"
picam.preview_configuration.align()
picam.configure("preview")
picam.start()

detected = 0 # variable que guarda el valor del numero detectado
introduced_password = ""
correct_password = "0000"
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
        cv2.putText(frame, f"Introduced passcode: {introduced_password}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
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


def password():
    time.sleep(1.5)
    global introduced_password
    global correct_password
    while True:
        entrada = input("Press d to save the detection, r to delete the detection or c to check the password: ")
        if entrada == "d" and len(introduced_password) < 4:
            introduced_password += str(detected)
        if entrada == "r" and introduced_password != "":
            introduced_password = introduced_password[:-1]
        if entrada == "c":
            if introduced_password == correct_password:
                print("¡The password is correct!")
                entrada = input('Press r to reset the password (or any other key to maintain it): ')
                if entrada == "r":
                    correct_password = None
                    while True:
                        try:
                            correct_password = input("Introduce the new correct password (format: 0000): ")
                            int(correct_password)
                            if len(correct_password) != 4:
                                print("Please intoduce a valid password")
                            else:
                                introduced_password = ""
                                break
                        except: 
                            print("Please intoduce a valid password")
                else:
                    introduced_password = ""
            else:
                print("The password is incorrect, please try again")
        


     


       
   
        
if __name__ == "__main__":

    try:
        photo_taker_thread = threading.Thread(target=photo_taker, daemon=True)  # Daemon=True para finalizar automáticamente con el programa
        stream_thread = threading.Thread(target=stream_video, daemon=True) 
        password_thread = threading.Thread(target=password, daemon=True) 
        photo_taker_thread.start()
        stream_thread.start()
        password_thread.start()
        photo_taker_thread.join()
        stream_thread.join()
        password_thread.join()
    except KeyboardInterrupt:
        pass
    
