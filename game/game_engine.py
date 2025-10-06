import pygame
from .paddle import Paddle
from .ball import Ball

WHITE = (255, 255, 255)

class GameEngine:
    WINNING_SCORE = 5

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)
        self.ball.engine = self  # allow ball to access sounds

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)

        self.game_over = False
        self.winner_message = ""

        # Initialize sounds (MP3s)
        pygame.mixer.init()
        self.sounds = {
            "paddle_hit": pygame.mixer.Sound("tennis-smash-100733.mp3"),
            "wall_bounce": pygame.mixer.Sound("ping-pong-ball-100074.mp3"),
            "score": pygame.mixer.Sound("point-smooth-beep-230573.mp3")
        }

    def play_sound(self, sound_name, max_time=200):
        """Play a sound effect for a limited duration (in milliseconds)."""
        if sound_name in self.sounds:
            self.sounds[sound_name].play(maxtime=max_time)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-self.player.speed, self.height)
        if keys[pygame.K_s]:
            self.player.move(self.player.speed, self.height)

    def update(self):
        if not self.game_over:
            self.ball.move()
            self.ball.check_collision(self.player, self.ai)

            if self.ball.x <= 0:
                self.ai_score += 1
                self.ball.reset()
                self.play_sound("score", 300)
            elif self.ball.x >= self.width:
                self.player_score += 1
                self.ball.reset()
                self.play_sound("score", 300)

            self.ai.auto_track(self.ball, self.height, smoothing=0.15)

            # Check Game Over
            self.check_game_over()

    def check_game_over(self):
        if self.player_score >= self.WINNING_SCORE:
            self.game_over = True
            self.winner_message = "Player Wins!"
        elif self.ai_score >= self.WINNING_SCORE:
            self.game_over = True
            self.winner_message = "AI Wins!"

    def display_game_over(self, screen):
        screen.fill((0, 0, 0))
        game_over_text = self.font.render(self.winner_message, True, WHITE)
        rect = game_over_text.get_rect(center=(self.width // 2, self.height // 2))
        screen.blit(game_over_text, rect)
        pygame.display.flip()
        pygame.time.delay(3000)

    def reset_game(self):
        self.player_score = 0
        self.ai_score = 0
        self.ball.reset()
        self.game_over = False
        self.winner_message = ""
        self.player.y = self.height // 2 - self.player.height // 2
        self.ai.y = self.height // 2 - self.ai.height // 2

    def replay_menu(self, screen):
        font = pygame.font.SysFont("Arial", 28)
        options = [
            "Best of 3 - Press 3",
            "Best of 5 - Press 5",
            "Best of 7 - Press 7",
            "Exit - Press ESC"
        ]

        menu_active = True
        while menu_active:
            screen.fill((0, 0, 0))
            for i, text in enumerate(options):
                rendered = font.render(text, True, WHITE)
                rect = rendered.get_rect(center=(self.width//2, self.height//2 - 60 + i*40))
                screen.blit(rendered, rect)

            pygame.display.flip()
            pygame.time.Clock().tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_3:
                        self.WINNING_SCORE = 2
                        menu_active = False
                    elif event.key == pygame.K_5:
                        self.WINNING_SCORE = 3
                        menu_active = False
                    elif event.key == pygame.K_7:
                        self.WINNING_SCORE = 4
                        menu_active = False
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()

        self.reset_game()

    def render(self, screen):
        self.player.draw(screen)
        self.ai.draw(screen)
        self.ball.draw(screen)
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # Draw scores
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))
