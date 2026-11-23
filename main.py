import math
import random

import cv2
import pygame

from bullet import Bullet
from coin import Coin
from obstacle import Obstacle
from player import Player
from road import Road
from vision.camera import get_camera_lane
from vision.movement import Movement
from vision.tracking import PoseTracker

pygame.init()


# camera initialization

pose_tracker = PoseTracker()
movement = Movement()


SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Glider")

clock = pygame.time.Clock()

road = Road()
player = Player(road)

PLAYER_Y = player.rect.centery

obstacles = []
OBSTACLE_SPAWN_INTERVAL = 700
obstacle_last_spawn_time = 0

coins = []
score = 0
COIN_SPAWN_INTERVAL = 500
coin_last_spawn_time = 0


bullets = []

game_over = False

def reset_game():
    global road, player, obstacles, coins, score, bullets, game_over
    global obstacle_last_spawn_time, coin_last_spawn_time
    
    road = Road()
    player = Player(road)
    obstacles = []
    coins = []
    score = 0
    bullets = []
    game_over = False
    obstacle_last_spawn_time = pygame.time.get_ticks()
    coin_last_spawn_time = pygame.time.get_ticks()


def spawn_obstacles():
    num_obstacles = random.randint(1, 2)

    for lane in random.sample([0, 1, 2], num_obstacles):
        obstacles.append(Obstacle(lane, road))

def spawn_coins():
    lane = random.randint(0, 2)

    for obstacle in obstacles:
        if obstacle.lane == lane and abs(obstacle.progress) < 0.15:
            return

    coins.append(Coin(lane, road))


font = pygame.font.Font(None, 36)
running = True
try:
    cap = cv2.VideoCapture(0)
    window_name = "Webcam Feed"

    if not cap.isOpened():
        print("Error: Could not open webcam")
        exit()  # noqa: PLR1722


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_SPACE:
                        reset_game()
                else:
                    if event.key == pygame.K_LEFT:
                        player.move_left()
                    elif event.key == pygame.K_RIGHT:
                        player.move_right() 
                    elif event.key == pygame.K_SPACE:
                        muzzle_x, muzzle_y = player.rect.midtop
                        print(muzzle_y, (muzzle_y - 150) / 650)
                        progress = math.sqrt((muzzle_y - 150) / 650)
                        bullets.append(Bullet(player.current_lane, road, progress, muzzle_x))

        lane, camera_frame = get_camera_lane(cap, pose_tracker, movement)

        if camera_frame is not None:
            cv2.imshow(window_name, camera_frame)
            cv2.waitKey(1)

            if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
                running = False


        if not game_over:
            if lane is not None:
                player.set_lane(lane)
            current_time = pygame.time.get_ticks()
            if (current_time - obstacle_last_spawn_time) >= OBSTACLE_SPAWN_INTERVAL:
                spawn_obstacles()
                obstacle_last_spawn_time = current_time
            if (current_time - coin_last_spawn_time) >= COIN_SPAWN_INTERVAL:
                spawn_coins()
                coin_last_spawn_time = current_time

            # keys = pygame.key.get_pressed()
            # player.jump(keys)
            player.update()
            road.update()

            for obstacle in obstacles[:]:
                obstacle.update()

                if obstacle.health <= 0:
                    score += 1

                if obstacle.progress >= 1 or obstacle.health <= 0:
                    obstacles.remove(obstacle)

                elif obstacle.is_at_player(PLAYER_Y) and obstacle.lane == player.current_lane:
                    game_over = True

            for coin in coins[:]:
                coin.update()

                if coin.progress >= 1:
                    coins.remove(coin)
                    continue

                if coin.is_at_player(PLAYER_Y) and coin.lane == player.current_lane:
                        score += 0.5
                        coins.remove(coin)
            for bullet in bullets[:]:
                bullet.update()

                for obstacle in obstacles[:]:
                    if bullet.lane == obstacle.lane and bullet.get_rect().colliderect(obstacle.get_rect()):
                        obstacle.health -= 1
                        bullets.remove(bullet)
                        break

                if bullet in bullets and bullet.progress <= 0.4:
                    bullets.remove(bullet)

        screen.fill("black")

        for obstacle in obstacles:
            obstacle.draw(screen)

        for coin in coins:
            coin.draw(screen)

        for bullet in bullets:
            bullet.draw(screen)

        player.draw(screen)

        coin_text = font.render(f"Score: {score}", True, "#CED4DA")
        screen.blit(coin_text, (20, 30))
        
        if game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))

            game_over_text = font.render("GAME OVER", True, (255, 80, 80))
            restart_text = font.render("Press Space to Restart", True, (255, 255, 255))
            final_score_text = font.render(
                f"Coins Collected: {score}",
                True,
                (255, 190, 40)
            )
            
            screen.blit(
                game_over_text,
                game_over_text.get_rect(center=(SCREEN_WIDTH // 2, 350))
            )
            screen.blit(
                restart_text,
                restart_text.get_rect(center=(SCREEN_WIDTH // 2, 450))
            )
            screen.blit(
                final_score_text,
                final_score_text.get_rect(center=(SCREEN_WIDTH // 2, 400))
            )

        pygame.display.flip()

        print("fps: ", clock.get_fps())
        clock.tick(60)

finally:
    cap.release()
    cv2.destroyAllWindows()
    pygame.quit()