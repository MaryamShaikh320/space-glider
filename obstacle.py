import pygame

from road import Road


class Obstacle:
    def __init__(self, lane, road):
        self.lane = lane
        self.progress = 0
        self.road = road
        self.health = 3

    def update(self):
        self.progress = self.progress + 0.005

    def get_position(self):
        y = 150 + 650 * (self.progress**2)
        lane_centers = self.road.get_lane_centers(y)
        x = lane_centers[self.lane]

        return (x, y)

    def get_rect(self):
        perspective_width = 10 + self.progress * 80
        perspective_height = 5 + self.progress * 80

        health_scale = self.health / 3

        width = perspective_width * health_scale
        height = perspective_height * health_scale

        x, y = self.get_position()

        rect_x = x - width / 2
        rect_y = y - height / 2

        return pygame.Rect(rect_x, rect_y, width, height)

    def get_color(self):
        if self.health == 3:
            return "#394654"
        elif self.health == 2:
            return "#4b5439"
        elif self.health == 1:
            return "#4d3a38"
        return "#000000"

    def draw(self, screen):
        pygame.draw.rect(screen, self.get_color(), self.get_rect(), 0, 10)

    def is_at_player(self, player_y):
        player_progress = ((player_y - 150) / 650) ** 0.5

        return abs(self.progress - player_progress) < 0.025