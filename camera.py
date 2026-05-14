# Her er et forsøg på en kamera fil. Jeg har som sagt ikke kameraet med hjem, så jeg aner ikke om det virker.
# Jeg fik efter lidt sparring at vide det ville være en god ide med en klasse til kameraet, så nu er der opsat
# en klasse - jeg er ikke sikker på om det overhovedet giver mening af have klasser med, men den er klar hvis vi
# ønsker det. Der er jo også "Stepper" klassen fra motor.py, som egentligt fungere ganske fint som den er.
# Jeg tænker at vi prøver det ad og snakker om det i morgen.
from picamera2 import Picamera2
from time import sleep
 
class Camera:
    def __init__(self):
        self.camera = Picamera2()
        # Kameraet konfigureres til video
        config = self.camera.create_video_configuration(
            main={"size": (1280, 720),  # 720p
                  "format": "RGB888"}   # RGB format som YOLO forventer
        )
        self.camera.configure(config)
    
    def start(self):
        self.camera.start()
        sleep(2)  # Giver kameraet tid til at varme op
        print("Kamera startet.")
    
    def get_frame(self):
        # Returnerer det nuværende frame som et "numpy array" - hvilket angiveligt er den format som Yolo ønsker/bruger
        frame = self.camera.capture_array()
        return frame
    
    def stop(self):
        self.camera.stop()
        self.camera.close()
        print("Kamera stoppet.")
