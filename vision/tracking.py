import time

import cv2
import mediapipe as mp
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.vision import drawing_utils


class PoseTracker:
    BaseOptions = mp.tasks.BaseOptions
    VisionRunningMode = mp.tasks.vision.RunningMode

    HandLandmarker = mp.tasks.vision.HandLandmarker
    HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions

    PoseLandmarker = mp.tasks.vision.PoseLandmarker
    PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions

    def __init__(self):
        self.poseOptions = self.PoseLandmarkerOptions(
            base_options=self.BaseOptions(model_asset_path="vision/pose_landmarker_lite.task"),
            running_mode=self.VisionRunningMode.VIDEO,
            num_poses=1
        )

        self.pose_landmarker = self.PoseLandmarker.create_from_options(self.poseOptions)


    def process_frame(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        timestamp = time.monotonic_ns() // 1_000_000

        detection_result = self.pose_landmarker.detect_for_video(mp_image, timestamp)

        if detection_result.pose_landmarks:
            landmarks = detection_result.pose_landmarks[0]

            drawing_utils.draw_landmarks(
                image=rgb_frame,
                landmark_list=landmarks,
                connections=vision.PoseLandmarksConnections.POSE_LANDMARKS
            )
            print("11.x", landmarks[11].x)
            print("11.y", landmarks[11].y)

            torso_center_x = self.get_torso_center_x(landmarks)

        new_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)

        return new_frame, torso_center_x

    def get_torso_center_x(self, landmarks):
        # 11->left shoulder 12->right shoulder 23->left hip 24->right hip
        return (landmarks[11].x + landmarks[12].x + landmarks[23].x + landmarks[24].x) / 4
        