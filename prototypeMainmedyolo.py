from motor import open_window, close_window, turn_on_fan, turn_off_fan, fan_setup, janitor
from humTemp import get_humTemp
from netConnect import do_connect
from pirsensor import pir_setup, read_pir
from time import sleep, time
from videoFeed import live_feed, kill_feed, start_feed, get_processed_frame
from yolo_functions import is_horse_down
from smokeADC import smoke_check
import numpy as np
import onnxruntime as ort

pir_setup()
fan_setup(9)
do_connect()
smoke_detected = None

horse_down_counter = 0
horse_was_laying = False
camera_active = False
motion_timer = None
fan_on = False
window_open = False
hum, temp = get_humTemp()
sensor_timer = time()
laying_frames = 0
laying_threshold = 3  

# Yolo setup, vi skal bruge onnx for bedste perfomance uden at brænda pi'en af.
yolo_session = ort.InferenceSession(
    "best.onnx",
    providers=["CPUExecutionProvider"]
)

input_name = yolo_session.get_inputs()[0].name
output_names = [o.name for o in yolo_session.get_outputs()]

try:
  while True:

    # Indsæt flask-kode imellem disse 2 kommentarer.

    # Indsæt flask-kode imellem disse 2 kommentarer.

    smoke_check()

    if smoke_detected:
      # Tænd for alarm på esp32
      close_window()
      turn_off_fan(9)

    else:
      if time() - sensor_timer > 1800:
        hum, temp = get_humTemp()
        sensor_timer = time()

      # --- Blæser kontrol
      if temp >= 24 and not fan_on:
        print("Høj temperatur, tænder blæser.")
        turn_on_fan(9)
        fan_on = True
      elif temp < 24 and fan_on:
        print("Temperatur acceptabel, slukker blæser.")
        turn_off_fan(9)
        fan_on = False

      # --- Vindue kontrol
      if hum >= 60 and not window_open:
        print("Høj fugtighed, åbner vindue.")
        open_window()
        window_open = True
      elif hum < 60 and window_open:
        print("Acceptabel luftfugtighed opnået, lukker vindue.")
        close_window()
        window_open = False

      # Status
      if not fan_on and not window_open and temp < 24 and hum < 60:
        print("Forhold er optimale, ingen handling påkrævet.")

    motion = read_pir()

    # Hvis ingen bevægelse opfanges - kun til sikring af kamera nedlukning.
    if not motion:
      motion_timer = None
      
      if camera_active:
        print("Ingen bevægelse — slukker kamera.")
        kill_feed()
        camera_active = False

    # Hvis bevægelse opfanges.
    else:
      if motion_timer is None:
        motion_timer = time()

      if not camera_active:
        print("Bevægelse registreret — starter kamera.")
        start_feed()
        camera_active = True

      if time() - motion_timer < 10:
        live_feed()

        # Yolo aflæsning ved brug af funktion fra yoloFunctions.py.
        frame_resized = get_processed_frame()

        if frame_resized is None:
          continue  # Spring denne iteration over og prøv igen.

        img = frame_resized.transpose(2, 0, 1)
        img = np.expand_dims(img, axis=0).astype(np.float32) / 255.0

        outputs = yolo_session.run(output_names, {input_name: img})
        yolo_result = is_horse_down(outputs)

        if yolo_result == "laying":
          laying_frames += 1

          if laying_frames >= laying_threshold:
            if not horse_was_laying:
              horse_down_counter += 1
              horse_was_laying = True

        else:
          laying_frames = 0
          horse_was_laying = False

      else:
        print("Ingen bevægelse i 10 sekunder — slukker kamera.")
        kill_feed()
        camera_active = False
        motion_timer = None

    sleep(0.5)
except KeyboardInterrupt:
  print("Program afbrudt, lukker ned.")
except Exception as e:
  print(f"Der opstod en fejl: {e}")
finally:
  janitor()
