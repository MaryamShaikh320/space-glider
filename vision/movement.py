import cv2
import mediapipe as mp


class Movement:
    def __init__(self):
        self.lanes = [0.33, 0.67, 1]
        self.current_lane = 1

    def update(self, frame, norm_torso_x, norm_torso_y, torso_x: int | None, torso_y: int | None):
        self.frame = frame
        self.norm_torso_x = float(norm_torso_x)
        self.norm_torso_y = float(norm_torso_y)
        self.torso_x = int(torso_x)
        self.torso_y = int(torso_y)

    def draw_torso_circle(self):
        cv2.circle(self.frame, (self.torso_x, self.torso_y), 10, (3, 144, 252))

    def get_normalized_torso_center(self):
        height, width = self.frame.shape[:2]

        return (self.torso_x / width), (self.torso_y / height)

    def get_lane(self):
        x = self.norm_torso_x
        
        if self.current_lane == 0:
            if x > 0.36:
                self.current_lane = 1
        elif self.current_lane == 1:
            if x < 0.30:
                self.current_lane = 0
            elif x > 0.70:
                self.current_lane = 2
        elif self.current_lane == 2:  # noqa: SIM102
            if x < 0.64:
                self.current_lane = 1

        return self.current_lane
    