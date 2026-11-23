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
            base_options=self.BaseOptions(
                model_asset_path="vision/pose_landmarker_lite.task"
            ),
            running_mode=self.VisionRunningMode.VIDEO,
            num_poses=1,
        )

        self.pose_landmarker = self.PoseLandmarker.create_from_options(self.poseOptions)

    def process_frame(self, frame, frame_dimensions):
        norm_x = None
        norm_y = None
        torso_center_x = None
        torso_center_y = None

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        timestamp = time.monotonic_ns() // 1_000_000

        detection_result = self.pose_landmarker.detect_for_video(mp_image, timestamp)

        if detection_result.pose_landmarks:
            landmarks = detection_result.pose_landmarks[0]

            # drawing_utils.draw_landmarks(
            #     image=rgb_frame,
            #     landmark_list=landmarks,
            #     connections=vision.PoseLandmarksConnections.POSE_LANDMARKS,
            # )

            norm_x, norm_y, torso_center_x, torso_center_y = self.get_torso_center(landmarks, frame_dimensions)

        new_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)

        return new_frame, norm_x, norm_y, torso_center_x, torso_center_y

    def get_torso_center(self, landmarks, frame_dimensions):
        # 11->left shoulder 12->right shoulder 23->left hip 24->right hip
        if (
            landmarks[11] is not None
            and landmarks[12] is not None
            and landmarks[23] is not None
            and landmarks[24] is not None
        ):
            height, width = frame_dimensions
            norm_x = (
                landmarks[11].x + landmarks[12].x + landmarks[23].x + landmarks[24].x
            ) / 4
            norm_y = (
                landmarks[11].y + landmarks[12].y + landmarks[23].y + landmarks[24].y
            ) / 4

            return norm_x, norm_y, (norm_x * width), (norm_y * height)

        return None, None
