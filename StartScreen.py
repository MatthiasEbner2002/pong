import pygame, sys, threading
from network import Network

class StartScreen:
    def __init__(self, window_width, window_height, window, clock):
        # Initialize Pygame
        #pygame.init() # This is already done in main.py

        # Set up the game window
        if window_width is not None:
            self.window_width = window_width
        else:
            self.window_width = 800
        
        if window_height is not None:
            self.window_height = window_height
        else:
            self.window_height = 600
            
        if window is not None:
            self.window = window
        else:
            self.window = pygame.display.set_mode((self.window_width, self.window_height))
        
        if clock is not None:
            self.clock = clock
        else:
            self.clock = pygame.time.Clock()
        
        pygame.display.set_caption("Start Screen")

        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GRAY = (128, 128, 128)
        self.GREEN = (0, 255, 0)
        
        # Game state
        self.game_state = "main_menu"

        # Game options
        self.options = ["START GAME", "JOIN GAME", "EXIT"]
        self.selected_option = 0
        
        # Network
        self.ip_address = ""
        
        # 
        self.connection_established = False
        self.network_thread = None
        self.network = None

    def run(self):

        while True:
            ret = self.render_screen()
            if ret is not None:
                return ret
            ret = self.handle_input()
            if ret is not None:
                return ret
            self.clock.tick(60)
            

    def render_screen(self):
        self.window.fill(self.BLACK) # Fill the screen with black

        
        if self.game_state == "main_menu":
            font_title = pygame.font.Font(None, 80)  # Increase font size for "Pong"
            font_options = pygame.font.Font(None, 40)
            title_text = font_title.render("Pong", True, self.WHITE)
            title_rect = title_text.get_rect(center=(self.window_width // 2, 100))
            
            self.option_texts = [font_options.render(option, True, self.WHITE) for option in self.options]

            self.option_rects = [
                option_text.get_rect(center=(self.window_width // 2, self.window_height // 2 + index * 50))
                for index, option_text in enumerate(self.option_texts)
            ]

            self.window.blit(title_text, title_rect)

            for index, option_rect in enumerate(self.option_rects):
                if option_rect.collidepoint(pygame.mouse.get_pos()):
                    self.selected_option = index
                    pygame.draw.rect(self.window, self.GRAY, option_rect)
                    pygame.draw.rect(self.window, self.BLACK, option_rect.inflate(6, 6))
                else:
                    pygame.draw.rect(self.window, self.BLACK, option_rect)

                if index == self.selected_option:
                    selected_option_react = option_rect
                    # Draw underline for hovered option
                    underline_rect = pygame.Rect(selected_option_react.left, selected_option_react.bottom - 4,
                                                selected_option_react.width, 4)
                    pygame.draw.rect(self.window, self.WHITE, underline_rect)

                self.window.blit(self.option_texts[index], option_rect)
                
        elif self.game_state == "join_game":
            font_title = pygame.font.Font(None, 80)
            font_input = pygame.font.Font(None, 40)

            title_text = font_title.render("Join Game", True, self.WHITE)
            title_rect = title_text.get_rect(center=(self.window_width // 2, 100))

            title_ip_text = font_input.render("Server IP:", True, self.WHITE)
            title_ip_rect = title_ip_text.get_rect(midleft=(self.window_width // 2 - 100, self.window_height // 2 - 50))

            pygame.draw.rect(self.window, self.WHITE, (self.window_width // 2 - 100, self.window_height // 2 - 25, 200, 50), 2)

            self.window.blit(title_text, title_rect)
            self.window.blit(title_ip_text, title_ip_rect)

            # Render the current IP address input
            ip_text = font_input.render(self.ip_address, True, self.WHITE)
            ip_rect = ip_text.get_rect(midleft=(self.window_width // 2 - 90, self.window_height // 2))
            self.window.blit(ip_text, ip_rect)

            
        elif self.game_state == "start_game":
            font_start = pygame.font.Font(None, 40)
            waiting_text = font_start.render("Waiting for a connection", True, self.WHITE)
            waiting_rect = waiting_text.get_rect(center=(self.window_width // 2, self.window_height // 2))
            ip_text = font_start.render(f"IP: {self.ip_address}", True, self.WHITE)
            ip_rect = ip_text.get_rect(center=(self.window_width // 2, self.window_height // 2 + 50))
            #print(self.ip_address)
            # Calculate the number of dots to display based on the current frame count
            num_dots = (pygame.time.get_ticks() // 500) % 4
            dots = "." * num_dots

            dots_text = font_start.render(dots, True, self.WHITE)
            dots_rect = dots_text.get_rect(left=waiting_rect.right + 10, centery=waiting_rect.centery)

            self.window.blit(waiting_text, waiting_rect)
            self.window.blit(dots_text, dots_rect)
            self.window.blit(ip_text, ip_rect)
        
            if self.connection_established:
                print(f"Network: {self.network}")
                return self.network
        
            
        pygame.display.flip()
        return None    

    def handle_input(self):
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if self.game_state == "main_menu":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % len(self.options) if self.selected_option is not None else 0
                    elif event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(self.options) if self.selected_option is not None else 0
                    elif event.key == pygame.K_RETURN:
                        if self.selected_option is not None:
                            print(f"Option {self.selected_option + 1} selected")
                            self.switch_to_option(self.options[self.selected_option])
                            # Add code for selected option action
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_pos = pygame.mouse.get_pos()
                    for index, option_rect in enumerate(self.option_rects):
                        if option_rect.collidepoint(mouse_pos):
                            self.selected_option = index
                            print(f"Option {self.selected_option + 1} selected")
                            self.switch_to_option(self.options[self.selected_option])
                            # Add code for selected option action
                            
            elif self.game_state == "join_game":
                 if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.ip_address = self.ip_address[:-1]  # Remove the last character
                    elif event.key == pygame.K_RETURN:
                        print(f"Connecting to server with IP: {self.ip_address}")
                        self.network:Network = Network(server_ip=self.ip_address)
                        return self.network
                        # Add code for connecting to the server with the entered IP address
                    else:
                        # Append the typed character to the IP address
                        if len(self.ip_address) < 15:  # Check the length of the IP address
                            self.ip_address += event.unicode

            elif self.game_state == "start_game":
                pass
        return None


    def switch_to_option(self, option):
        if option == "START GAME":
            self.network_thread = threading.Thread(target=self.wait_for_connection)
            self.network_thread.start()
            self.game_state = "start_game"
        elif option == "JOIN GAME":
            self.game_state = "join_game"
        elif option == "EXIT":
            pygame.quit()
            sys.exit()
            
    def wait_for_connection(self):
        self.network = Network(is_server=True, start_now=False)
        self.ip_address = self.network.start_socket()

        #while not self.connection_established:
        self.network.accept_connection()
        self.connection_established = True


# Create an instance of the StartScreen class and run the game
#start_screen = StartScreen()
#start_screen.run()
