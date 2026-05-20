from camera import Camera
import cv2

camera = Camera()

def live_feed():
    frame = cam.get_frame()

    if frame is None:
        return None
    
    cv2.waitKey(1)
    cv2.imshow("Kamera Test", frame)

    return frame

def kill_feed():
    camera.stop()
    cv2.destroyAllWindows()
    
