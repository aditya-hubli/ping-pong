import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-7, 7])
        self.velocity_y = random.choice([-4, 4])
        self.engine = None  # To be set by GameEngine for sound access

    def move(self):
        old_x, old_y = self.x, self.y
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Wall bounce
        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1
            self.y = max(0, min(self.y, self.screen_height - self.height))
            if self.engine:
                self.engine.play_sound("wall_bounce", 150)

        # Keep motion line for accurate collision
        self.motion_line = ((old_x, old_y), (self.x, self.y))

    def check_collision(self, player, ai):
        ball_rect = self.rect()
        for paddle in (player, ai):
            paddle_rect = paddle.rect()

            if not ball_rect.colliderect(paddle_rect):
                if not paddle_rect.clipline(self.motion_line):
                    continue

            # Collision confirmed - check direction BEFORE reversing
            moving_right = self.velocity_x > 0
            
            # Adjust position outside paddle BEFORE reversing velocity
            if moving_right:
                # Ball was moving right, hit AI paddle, push it left
                self.x = paddle_rect.left - self.width - 1
            else:
                # Ball was moving left, hit player paddle, push it right
                self.x = paddle_rect.right + 1

            # Now reverse velocity
            self.velocity_x *= -1

            # Slight Y deflection with cap
            offset = (self.y + self.height / 2) - (paddle.y + paddle.height / 2)
            self.velocity_y += offset * 0.05
            
            # Cap velocities to prevent runaway speed
            max_speed_x = 12
            max_speed_y = 8
            self.velocity_x = max(-max_speed_x, min(self.velocity_x, max_speed_x))
            self.velocity_y = max(-max_speed_y, min(self.velocity_y, max_speed_y))

            # Play paddle hit sound
            if self.engine:
                self.engine.play_sound("paddle_hit", 200)

            break

    def reset(self):
        self.x = self.screen_width / 2 - self.width / 2
        self.y = self.screen_height / 2 - self.height / 2
        self.velocity_x = random.choice([-7, 7])
        self.velocity_y = random.choice([-4, 4])

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, surface):
        pygame.draw.ellipse(surface, (255, 255, 255), self.rect())
