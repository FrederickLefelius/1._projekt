<<<<<<< HEAD
import cv2
from picamera2 import Picamera2
from time import sleep


class Camera:
    def __init__(self):
        self.camera = Picamera2()
        config = self.camera.create_video_configuration(
            main={"size": (1280, 720),
                  "format": "RGB888"}
        )
        self.camera.configure(config)

    def start(self):
        self.camera.start()
        sleep(2)
        print("Kamera startet.")

    def get_frame(self):
        """Return the current frame as a raw numpy array."""
        return self.camera.capture_array()

    def get_jpeg(self):
        """Return the current frame encoded as JPEG bytes for streaming."""
        frame = self.camera.capture_array()
        _, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

    def stop(self):
        self.camera.stop()
        self.camera.close()
        print("Kamera stoppet.")


def stream_camera(socketio):
    """
    Background thread: captures frames and emits them to all
    connected WebSocket clients as base64-encoded JPEGs.
    """
    cam = Camera()
    try:
        cam.start()
        import base64
        while True:
            jpeg = cam.get_jpeg()
            b64  = base64.b64encode(jpeg).decode('utf-8')
            socketio.emit('camera_frame', {'frame': b64})
            sleep(0.05)  # ~20 fps
    except Exception as e:
        print(f"Camera stream error: {e}")
    finally:
=======
import cv2
from picamera2 import Picamera2
from time import sleep


class Camera:
    def __init__(self):
        self.camera = Picamera2()
        config = self.camera.create_video_configuration(
            main={"size": (1280, 720),
                  "format": "RGB888"}
        )
        self.camera.configure(config)

    def start(self):
        self.camera.start()
        sleep(2)
        print("Kamera startet.")

    def get_frame(self):
        """Return the current frame as a raw numpy array."""
        return self.camera.capture_array()

    def get_jpeg(self):
        """Return the current frame encoded as JPEG bytes for streaming."""
        frame = self.camera.capture_array()
        _, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

    def stop(self):
        self.camera.stop()
        self.camera.close()
        print("Kamera stoppet.")


def stream_camera(socketio):
    """
    Background thread: captures frames and emits them to all
    connected WebSocket clients as base64-encoded JPEGs.
    """
    cam = Camera()
    try:
        cam.start()
        import base64
        while True:
            jpeg = cam.get_jpeg()
            b64  = base64.b64encode(jpeg).decode('utf-8')
            socketio.emit('camera_frame', {'frame': b64})
            sleep(0.05)  # ~20 fps
    except Exception as e:
        print(f"Camera stream error: {e}")
    finally:
>>>>>>> fdf27f7ae133e92063dfe14a4ce68fc18fdc4830
        cam.stop()