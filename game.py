import pygame
import random
import math
from network import Network
from SendData import SendData
from StartScreen import StartScreen

class Game:
    def __init__(self, screen_width, screen_height, network: Network=None):
        # Initialize the game
        pygame.init()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()

        # Initialize the network
        self.is_server = True  # Set to True if this instance is the server

        if network is None:
            start_screen: StartScreen = StartScreen(self.screen_width, self.screen_height, self.screen, self.clock)
            self.network = start_screen.run()
            print(self.network.is_server)
            
        
        # Game variables
        self.paddle1_pos = self.screen_height // 2
        self.paddle2_pos = self.screen_height // 2
        self.paddle_speed = 8

        self.ball_x = self.screen_width // 2
        self.ball_y = self.screen_height // 2
        self.ball_dx = 5 if random.random() < 0.5 else -5
        self.ball_dy = 5 if random.random() < 0.5 else -5

        self.ball_size = 20

        self.player1_score = 0
        self.player2_score = 0

        self.game_state = "start"

    def calculate_ball_angle(self, paddle_pos, ball_pos):
        relative_y = ball_pos - paddle_pos
        normalized_relative_y = (relative_y - 25) / 25
        max_angle = math.pi * 3 / 4
        angle = math.sin(normalized_relative_y * math.pi / 2) * max_angle
        return -angle

    def reset_game(self):
        self.ball_x = self.screen_width // 2
        self.ball_y = self.screen_height // 2
        self.ball_dx = 5 if random.random() < 0.5 else -5
        self.ball_dy = 5 if random.random() < 0.5 else -5

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if self.game_state == "start":
                    if event.key == pygame.K_SPACE:
                        self.game_state = "playing"
                elif self.game_state == "game_over":
                    if event.key == pygame.K_SPACE:
                        self.game_state = "start"
                        self.player1_score = 0
                        self.player2_score = 0
                        self.reset_game()
        return True

    def update_game(self, keys):
        if self.game_state == "playing":
            if self.network.is_server:
                if keys[pygame.K_w] and self.paddle1_pos > 0:
                    self.paddle1_pos -= self.paddle_speed
                if keys[pygame.K_s] and self.paddle1_pos < self.screen_height - 50:
                    self.paddle1_pos += self.paddle_speed
            else:
                if keys[pygame.K_UP] and self.paddle2_pos > 0:
                    self.paddle2_pos -= self.paddle_speed
                if keys[pygame.K_DOWN] and self.paddle2_pos < self.screen_height - 50:
                    self.paddle2_pos += self.paddle_speed

            if self.network.is_server:

                self.ball_x += self.ball_dx
                self.ball_y += self.ball_dy

                if self.ball_x < 0:
                    self.player2_score += 1
                    self.reset_game()
                elif self.ball_x > self.screen_width:
                    self.player1_score += 1
                    self.reset_game()

                if self.player1_score >= 10 or self.player2_score >= 10:
                    self.game_state = "game_over"

                if self.ball_y <= self.ball_size // 2 or self.ball_y >= self.screen_height - 1 - self.ball_size // 2:
                    self.ball_dy *= -1

                if self.ball_x == 30 and self.paddle1_pos <= self.ball_y < self.paddle1_pos + 50:
                    ball_angle = self.calculate_ball_angle(self.paddle1_pos, self.ball_y)
                    self.ball_dx = abs(self.ball_dx)
                    self.ball_dy = -math.sin(ball_angle) * 5
                    self.ball_dy += random.uniform(-1, 1)
                if self.ball_x == self.screen_width - 50 and self.paddle2_pos <= self.ball_y < self.paddle2_pos + 50:
                    ball_angle = self.calculate_ball_angle(self.paddle2_pos, self.ball_y)
                    self.ball_dx = -abs(self.ball_dx)
                    self.ball_dy = -math.sin(ball_angle) * 5
                    self.ball_dy += random.uniform(-1, 1)

            # Send and receive player positions
            if self.network.is_server:
                data: SendData = SendData(self.paddle1_pos, self.game_state, self.ball_x, self.ball_y, self.player1_score, self.player2_score)
                self.network.send_data(data)
                self.paddle2_pos = self.network.receive_data()
                
            else:
                data:SendData = self.network.receive_data()
                self.paddle1_pos = data.player_position
                self.ball_x = data.ball_x
                self.ball_y = data.ball_y
                self.game_state = data.game_state
                self.player1_score = data.server_score
                self.player2_score = data.client_score
                self.network.send_data(self.paddle2_pos)
                

    def render_game(self):
        self.screen.fill((0, 0, 0))
        if self.game_state == "start":
            start_font = pygame.font.Font(None, 36)
            start_text = start_font.render("Press SPACE to start", True, (255, 255, 255))
            self.screen.blit(start_text, (self.screen_width // 2 - start_text.get_width() // 2, self.screen_height // 2))
        elif self.game_state == "playing":
            pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(20, self.paddle1_pos, 10, 50))
            pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(self.screen_width - 40, self.paddle2_pos, 10, 50))
            pygame.draw.circle(self.screen, (255, 255, 255), (self.ball_x, self.ball_y), self.ball_size // 2)
            score_font = pygame.font.Font(None, 36)
            player1_text = score_font.render("Player 1: " + str(self.player1_score), True, (255, 255, 255))
            player2_text = score_font.render("Player 2: " + str(self.player2_score), True, (255, 255, 255))
            self.screen.blit(player1_text, (10, 10))
            self.screen.blit(player2_text, (self.screen_width - player2_text.get_width() - 10, 10))
        elif self.game_state == "game_over":
            start_font = pygame.font.Font(None, 36)
            game_over_font = pygame.font.Font(None, 48)
            game_over_text = game_over_font.render("Game Over", True, (255, 255, 255))
            self.screen.blit(game_over_text, (self.screen_width // 2 - game_over_text.get_width() // 2, self.screen_height // 2 - game_over_text.get_height() // 2))
            restart_text = start_font.render("Press SPACE to restart", True, (255, 255, 255))
            self.screen.blit(restart_text, (self.screen_width // 2 - restart_text.get_width() // 2, self.screen_height // 2 + restart_text.get_height() // 2))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            keys = pygame.key.get_pressed()

            running = self.handle_events()

            self.update_game(keys)

            self.render_game()

            self.clock.tick(60)

        pygame.quit()
        return self.network
