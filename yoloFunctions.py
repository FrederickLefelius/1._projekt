import math
import numpy as np
from collections import deque

# keeps last results for smoothing
pose_history = deque(maxlen=5)

def is_horse_down(outputs):
    data = outputs[0]

    if data is None or len(data) == 0:
        return None

    det = data[0]

    keypoints = det[5:]

    # need at least a few keypoints
    if len(keypoints) < 10:
        return None

    # helper: get point safely
    def pt(i):
        return keypoints[i], keypoints[i + 1]

    # pick multiple body points (more stable than 2-point method)
    try:
        head = pt(0)
        mid1 = pt(len(keypoints)//4)
        mid2 = pt(len(keypoints)//2)
        rear = pt(3*len(keypoints)//4)
    except IndexError:
        return None

    # compute multiple angles
    def angle(a, b):
        return abs(math.degrees(math.atan2(b[1]-a[1], b[0]-a[0])))

    angles = [
        angle(head, mid2),
        angle(mid1, mid2),
        angle(mid2, rear)
    ]

    avg_angle = sum(angles) / len(angles)

    # classify
    is_laying_now = (avg_angle < 35 or avg_angle > 145)

    # temporal smoothing
    pose_history.append(is_laying_now)

    # require majority vote over last frames
    if pose_history.count(True) >= 3:
        return "laying"
    elif pose_history.count(False) >= 3:
        return "standing"

    return None
  
