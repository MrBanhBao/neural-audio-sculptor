
import mediapipe as mp
import numpy as np
from PIL import Image

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose


def calc_landmarks_and_annotate(image):
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


        circle_radius = int(.02 * np_image.shape[1])

        point_spec = mp_drawing.DrawingSpec(color=(220, 100, 0), thickness=-1, circle_radius=circle_radius)
        line_spec = mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2)

        mp_drawing.draw_landmarks(
            np_image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=point_spec,
            connection_drawing_spec=line_spec)

        return Image.fromarray(np.uint8(np_image))