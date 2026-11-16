import pygame

from road import Road


class Bullet:
    def __init__(self, lane, road, progress, start_x):
        self.lane = lane
        self.road = road
        self.start_progress = progress
        self.progress = progress
        self.start_x = start_x
        self.speed = 0.01

    def update(self):
        self.progress -= self.speed

    def get_position(self):
        y = 150 + 650 * (self.progress**2)

        road_left_x = self.road.interpolate_x(
            y, self.road.road_points[0], self.road.road_points[3]
        )
        left_divider_x = self.road.interpolate_x(
            y, self.road.left_divider[0], self.road.left_divider[1]
        )
        right_divider_x = self.road.interpolate_x(
            y, self.road.right_divider[0], self.road.right_divider[1]
        )
        road_right_x = self.road.interpolate_x(
            y, self.road.road_points[1], self.road.road_points[2]
        )

        lane_centers = [
            (road_left_x + left_divider_x) / 2,
            (left_divider_x + right_divider_x) / 2,
            (right_divider_x + road_right_x) / 2,
        ]

        x = lane_centers[self.lane]
    
        return (x, y)

        return (x, y)

    def get_rect(self):
        width = 2 + self.progress * 8
        height = 3 + self.progress * 12

        x, y = self.get_position()

        rect_x = x - width / 2
        rect_y = y - height / 2

        return pygame.Rect(rect_x, rect_y, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, "#FFFFFF", self.get_rect())