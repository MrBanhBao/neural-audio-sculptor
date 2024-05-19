
import mediapipe as mp
import numpy as np
from PIL import Image

import utils.store as store
from data_models import Landmark

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

prev_results = None

POSE_LANDMARKS = {
    0: "nose",
    1: "left_eye_inner",
    2: "left_eye",
    3: "left_eye_outer",
    4: "right_eye_inner",
    5: "right_eye",
    6: "right_eye_outer",
    7: "left_ear",
    8: "right_ear",
    9: "mouth_left",
    10: "mouth_right",
    11: "left_shoulder",
    12: "right_shoulder",
    13: "left_elbow",
    14: "right_elbow",
    15: "left_wrist",
    16: "right_wrist",
    17: "left_pinky",
    18: "right_pinky",
    19: "left_index",
    20: "right_index",
    21: "left_thumb",
    22: "right_thumb",
    23: "left_hip",
    24: "right_hip",
    25: "left_knee",
    26: "right_knee",
    27: "left_ankle",
    28: "right_ankle",
    29: "left_heel",
    30: "right_heel",
    31: "left_foot_index",
    32: "right_foot_index"
}

def calc_landmarks_and_annotate(image):
    global prev_results
    with mp_pose.Pose(
            static_image_mode=False,
            model_complexity=0,
            smooth_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as pose:


        np_image = np.array(image)
        results = pose.process(np_image)

        if not results.pose_landmarks:
            return image
        else:
            for idx, landmark in enumerate(results.pose_landmarks.landmark):
                delta_landmarks = calculate_diff(results, idx)
                name = POSE_LANDMARKS[idx]

                store.delta_pose_landmarks[name] = delta_landmarks
                store.pose_landmarks[name] = Landmark(x=landmark.x-0.5, y=landmark.y-0.5, z=landmark.z)

        prev_results = results

        circle_radius = int(.015 * np_image.shape[1])

        point_spec = mp_drawing.DrawingSpec(color=(220, 100, 0), thickness=-1, circle_radius=circle_radius)
        line_spec = mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2)

        mp_drawing.draw_landmarks(
            np_image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=point_spec,
            connection_drawing_spec=line_spec)

        return Image.fromarray(np.uint8(np_image))

def calculate_diff(results, landmark=mp_pose.PoseLandmark.NOSE) -> Landmark:
    global prev_results
    if prev_results is not None:
        if hasattr(results.pose_landmarks, "landmark") and hasattr(prev_results.pose_landmarks, "landmark"):
            landmark_x = results.pose_landmarks.landmark[landmark].x
            landmark_y = results.pose_landmarks.landmark[landmark].y
            landmark_z = results.pose_landmarks.landmark[landmark].z

            prev_landmark_x = prev_results.pose_landmarks.landmark[landmark].x
            prev_landmark_y = prev_results.pose_landmarks.landmark[landmark].y
            prev_landmark_z = prev_results.pose_landmarks.landmark[landmark].z

            return Landmark(x=prev_landmark_x-landmark_x, y=prev_landmark_y-landmark_y, z=prev_landmark_z-landmark_z)