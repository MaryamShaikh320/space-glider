import cv2
import mediapipe as mp


class Movement:
    # def __init__(self):

    def update(self, frame, torso_x: int | None, torso_y: int | None):
        self.frame = frame
        self.torso_x = int(torso_x)
        self.torso_y = int(torso_y)

    def draw_torso_circle(self):
        cv2.circle(self.frame, (self.torso_x, self.torso_y), 10, (3, 144, 252))