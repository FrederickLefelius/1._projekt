import math
from collections import deque

# Gemmer de sidste resultater for at udjævne udsving
pose_history = deque(maxlen=5)

def is_horse_down(outputs):
    # ONNX returnerer en liste af numpy arrays
    # outputs[0] har formen: (1, antal_detektioner, data_per_detektion)
    if outputs is None or len(outputs) == 0:
        return None

    data = outputs[0]

    # Fjern batch dimension: (1, N, D) -> (N, D)
    if len(data.shape) == 3:
        data = data[0]

    # Tjek om der er nogen detektioner
    if len(data) == 0:
        return None

    # Tag den første detektion
    det = data[0]

    # ONNX pose format: [x, y, w, h, conf, kp1_x, kp1_y, kp1_conf, kp2_x, ...]
    # Keypoints starter ved index 5, hver keypoint har 3 værdier (x, y, conf)
    keypoints_raw = det[5:]

    # Hent x,y koordinater for hvert keypoint (spring conf over)
    keypoints = [(keypoints_raw[i], keypoints_raw[i+1]) 
                 for i in range(0, len(keypoints_raw) - 2, 3)]

    # Tjek om der er nok keypoints
    if len(keypoints) < 4:
        return None

    # Hjælpefunktion til at hente et punkt
    def pt(i):
        return float(keypoints[i][0]), float(keypoints[i][1])

    # Hjælpefunktion til at beregne vinkel mellem to punkter
    def angle(a, b):
        return abs(math.degrees(math.atan2(b[1] - a[1], b[0] - a[0])))

    try:
        # Hent punkter fordelt over hestens krop
        head = pt(0)
        mid1 = pt(len(keypoints) // 4)
        mid2 = pt(len(keypoints) // 2)
        rear = pt(3 * len(keypoints) // 4)
    except IndexError:
        return None

    # Tjek om keypoints er gyldige (ikke 0,0)
    if any(x == 0.0 and y == 0.0 for x, y in [head, mid1, mid2, rear]):
        return None

    # Beregn vinkler mellem punkterne
    angles = [
        angle(head, mid2),
        angle(mid1, mid2),
        angle(mid2, rear)
    ]

    # Mål kun vinklen mellem hoved og bagkrop - den mest betydningsfulde vinkel
    main_angle = angle(head, rear)

    print(f"Hoved-til-bagkrop vinkel: {main_angle:.1f} grader")

    # Stående hest: kroppen er lodret (~90 grader)
    # Liggende hest: kroppen er vandret (~0 eller ~180 grader)
    is_laying_now = (main_angle < 45 or main_angle > 135)

    # Tilføj til historik for temporal smoothing
    pose_history.append(is_laying_now)

    # Kræv flertal over de sidste frames før vi konkluderer
    if pose_history.count(True) >= 3:
        return "laying"
    elif pose_history.count(False) >= 3:
        return "standing"

    return None
    
