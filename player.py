
import pygame


class Player:
    def __init__(self):
        self.gunner_surface = pygame.Surface((60, 120), pygame.SRCALPHA)
        pygame.draw.polygon(
            self.gunner_surface,
            "#00E5FF",
            [
                (0, 120),
                (0, 50),
                (20, 0),
                (40, 0),
                (60, 50),
                (60, 120)
            ]
        )
        
        pygame.draw.polygon(
            self.gunner_surface, 
            "#6e6e6e", 
            [
                (0, 120),
                (0, 50),
                (20, 0),
                (40, 0),
                (60, 50),
                (60, 120)
            ],
            10
        )
        self.rect = self.gunner_surface.get_rect(center=(305, 620))

        # # Jump physics
        # self.vertical_velocity = 0
        # self.on_ground = True
        # self.gravity = 1
        # self.jump_velocity = -15
        # self.jump_height = 0

        # Lane movement
        self.current_lane = 1
        self.lane_positions = [105, 305, 505]

        #glow surfaces
        self.player_glow_surface = self.create_glow(100, (41, 255, 139), 200)
        self.slots_glow_surface = self.create_glow(50, (121, 198, 237), 200)
    
    def update(self):
        target_center_x = self.lane_positions[self.current_lane]

        if self.rect.centerx < target_center_x:
            self.rect.centerx = min(self.rect.centerx + 15, target_center_x)
        elif self.rect.centerx > target_center_x:
            self.rect.centerx = max(self.rect.centerx - 15, target_center_x)

    def get_hitbox(self):
        return self.rect

    def move_left(self):
        self.current_lane = max(0, self.current_lane - 1)

    def move_right(self):
        self.current_lane = min(self.current_lane + 1, 2)

    # def jump(self, keys):
    #     if keys[pygame.K_UP] and self.on_ground:
    #         self.vertical_velocity = self.jump_velocity
    #         self.on_ground = False

    def draw(self, screen):
        # ship
        pygame.draw.rect(screen, "#6e6e6e", (50, 623, 500, 20))
        pygame.draw.rect(screen, "#6e6e6e", (40, 503, 10, 260), 0, 5)
        pygame.draw.rect(screen, "#6e6e6e", (550, 503, 10, 260))

        # track
        center_x = self.rect.centerx
        center_y = 633

        pygame.draw.line(
            screen,
            "#3d3d3d",
            (50, 623),
            (center_x, center_y),
            3
        )

        pygame.draw.line(
            screen,
            "#3d3d3d",
            (center_x, center_y),
            (550, 643),
            3
        )

        pygame.draw.line(
            screen,
            "#3d3d3d",
            (50, 643),
            (center_x, center_y),
            3
        )

        pygame.draw.line(
            screen,
            "#3d3d3d",
            (center_x, center_y),
            (550, 623),
            3
        )

        # ship slots
        # have to do some special positioning because lane position are based on the center not top left
        for i in range(3):
            slot_center = (self.lane_positions[i], 632)
            glow_rect = self.slots_glow_surface.get_rect(center=slot_center)
            screen.blit(self.slots_glow_surface, glow_rect)

            outer_rect = pygame.Rect(0, 0, 25, 25)
            outer_rect.center = slot_center
            pygame.draw.rect(screen, "#474747", outer_rect, 3, 5)

            inner_rect = pygame.Rect(0, 0, 19, 19)
            inner_rect.center = slot_center
            pygame.draw.rect(screen, "black", inner_rect)

            # screen.blit(self.slots_glow_surface, (self.lane_positions[i], 547))
            # pygame.draw.rect(screen, "#474747", (self.lane_positions[i] + 12, 560, 25, 25), 3, 5)
            # pygame.draw.rect(screen, "black", (self.lane_positions[i] + 15, 563, 19, 19))

        # player
        screen.blit(self.gunner_surface, self.rect.topleft)

        # visual_rect = self.rect.copy()
        # visual_rect.y -= int(self.jump_height)

        # glow_x = visual_rect.centerx - 50
        # glow_y = visual_rect.centery - 50

        # screen.blit(self.player_glow_surface, (glow_x, glow_y))

        # pygame.draw.rect(
        #     screen, (41, 255, 139), visual_rect, 0, 15
        # )

        # pygame.draw.ellipse(
        #     screen,
        #     (160, 255, 190),
        #     (visual_rect.left + 3, visual_rect.top + 5, 20, 7)
        # )

    def create_glow(self, size, rgb, alpha_scale=255):
            center = size / 2
            radius = size / 2
    
            glow = pygame.Surface((size, size), pygame.SRCALPHA)
    
            for x in range(size):
                for y in range(size):
                    distance = ((x - center) ** 2 + (y - center) ** 2) ** 0.5
    
                    alpha = max(0, int(alpha_scale * (1 - distance / radius)))

                    color = rgb + (alpha,)
    
                    glow.set_at((x, y), color)
    
            return glow