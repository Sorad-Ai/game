import cv2
import mediapipe as mp
from django.http import StreamingHttpResponse
from django.shortcuts import render
import numpy as np
import time
import pyautogui

# Initialize MediaPipe components
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Example ground truth positions for landmarks
def get_ground_truth_positions():
    return {
        0: (0.5, 0.5),  # Example position for landmark 0
        1: (0.4, 0.4),  # Example position for landmark 1
    }

def calculate_accuracy(detected_landmarks, true_positions):
    detected_positions = np.array([(lm.x, lm.y) for lm in detected_landmarks])
    true_positions_list = [true_positions.get(i, (0, 0)) for i in range(len(detected_landmarks))]
    true_positions = np.array(true_positions_list)
    distances = np.linalg.norm(detected_positions - true_positions, axis=1)
    avg_distance = np.mean(distances) if len(distances) > 0 else 0
    accuracy = max(0, 100 - avg_distance * 100)
    return accuracy

def is_finger_pose(finger_tip, finger_base):
    """Check if a finger is curled based on its tip and base positions."""
    return finger_tip.y > finger_base.y

def calculate_angle(v1, v2):
    """Calculate the angle between two vectors."""
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    cos_theta = dot_product / (norm_v1 * norm_v2)
    angle = np.arccos(np.clip(cos_theta, -1.0, 1.0))
    return np.degrees(angle)

def detect_fist(landmarks):
    thumb_tip = landmarks[4]
    thumb_base = landmarks[2]
    index_tip = landmarks[8]
    index_base = landmarks[5]
    middle_tip = landmarks[12]
    middle_base = landmarks[9]
    ring_tip = landmarks[16]
    ring_base = landmarks[13]
    little_tip = landmarks[20]
    little_base = landmarks[18]

    # Check if the thumb, index, middle, ring, and little fingers are curled (fist)
    # thumb_curled = is_finger_curled(thumb_tip, thumb_base)
    index_curled = is_finger_pose(index_tip, index_base)
    middle_curled = is_finger_pose(middle_tip, middle_base)
    ring_curled = is_finger_pose(ring_tip, ring_base)
    little_curled = is_finger_pose(little_tip, little_base)

    # For check pose form f(x)  /////////// fist
    is_fist =  index_curled and middle_curled and ring_curled and little_curled
    index_up = is_finger_pose(index_tip, index_base)

    # For up gest
    index_up = index_tip.y < index_base.y
    is_fist1 = middle_curled and ring_curled and little_curled

    # For right gest
    little_up = little_tip.y < little_base.y
    is_fist2 = index_curled and middle_curled and ring_curled
    
    # Calculate angle for left gesture detection
    v1 = np.array([thumb_tip.x - thumb_base.x, thumb_tip.y - thumb_base.y])
    v2 = np.array([index_tip.x - thumb_base.x, index_tip.y - thumb_base.y])
    angle = calculate_angle(v1, v2)

    # Define a threshold angle for the left gesture
    threshold_angle = 70
    is_fist3 = index_curled and middle_curled and ring_curled

    # For down gest
    ring_up = ring_tip.y < ring_base.y

    if index_curled and middle_curled and little_up and ring_up:
        # time.sleep(0.01)
        pyautogui.hotkey('s')
        return "Down Gesture"
    
    if angle > threshold_angle and is_fist3:
        pyautogui.hotkey('a')
        return "Left Gesture"
    
    if is_fist2 and little_up:
        pyautogui.hotkey('d')
        return "Right Gesture"
    
    if is_fist1 and index_up:
        pyautogui.hotkey('w')
        return "Up Gesture"
    
    if is_fist:
        return "Fist"
    
    pyautogui.hotkey('space')
    return "No Fist"

def gen(show_accuracy=True):
    time.sleep(1)
    cap = cv2.VideoCapture(0)
    
    with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb_frame)

            if results.multi_hand_landmarks:
                landmarks = results.multi_hand_landmarks[0]
                
                # Fist detection
                fist = detect_fist(landmarks.landmark)
                cv2.putText(frame, f'Gesture: {fist}', (10, 60), cv2.FONT_HERSHEY_COMPLEX, 0.75, (255, 255, 0), 2)
                
                if show_accuracy:
                    # Draw hand tracking lines and show accuracy text on the original frame
                    mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)
                    true_positions = get_ground_truth_positions()
                    accuracy = calculate_accuracy(landmarks.landmark, true_positions)
                    cv2.putText(frame, f'Accuracy: {accuracy:.2f}%', (10, 30), cv2.FONT_HERSHEY_COMPLEX, 0.75, (255, 255, 0), 2)

                # Draw hand tracking points with red border on the original frame
                for landmark in landmarks.landmark:
                    x, y = int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])
                    cv2.circle(frame, (x, y), 1, (0, 0, 255), 2)  # Red border with thickness 1

            # Encode the frame as a PNG image
            ret, png = cv2.imencode('.png', frame)
            if not ret:
                continue

            yield (b'--frame\r\n'
                   b'Content-Type: image/png\r\n\r\n' + png.tobytes() + b'\r\n')
    
    cap.release()

def video_feed(request):
    show_accuracy = request.GET.get('show_accuracy', 'false').lower() == 'true'
    return StreamingHttpResponse(gen(show_accuracy), content_type='multipart/x-mixed-replace; boundary=frame')

def index(request):
    return render(request, 'index.html')
