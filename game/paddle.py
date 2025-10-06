import pygame

class Paddle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 8

    def move(self, dy, screen_height):
        self.y += dy
        self.y = max(0, min(self.y, screen_height - self.height))

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def auto_track(self, ball, screen_height, smoothing=0.5):
        """AI tracking with optional smoothing factor."""
        # Only track if ball is moving towards AI (velocity_x > 0 for right paddle)
        if ball.velocity_x > 0:
            center_diff = (ball.y - (self.y + self.height / 2))
            movement = center_diff * smoothing
            # Cap AI movement speed to prevent jitter
            max_speed = self.speed * 1.2
            movement = max(-max_speed, min(movement, max_speed))
            self.move(movement, screen_height)
        else:
            # Return to center when ball is moving away
            center_y = screen_height / 2 - self.height / 2
            center_diff = center_y - self.y
            movement = center_diff * 0.08  # Slow return to center
            self.move(movement, screen_height)

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), self.rect())
