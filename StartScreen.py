import pygame, sys, threading
from typing import Dict, List, Optional
from network import Network
from SettingData import SettingData

class StartScreen:
    def __init__(self, window_width, window_height, window, clock):
        
        # Set up the game window
        if window_width is not None:
            self.window_width: int = window_width
        else:
            self.window_width: int = 800
        
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
            self.clock: pygame.time.Clock = pygame.time.Clock()
        
        pygame.display.set_caption("Start Screen") # Set the caption of the window

        # Colors
        self.BLACK  = (0, 0, 0)
        self.WHITE  = (255, 255, 255)
        self.GRAY   = (128, 128, 128)
        self.GREEN  = (0, 255, 0)
        self.RED    = (255, 0, 0)
        self.BLUE   = (0, 0, 255)
        self.YELLOW = (255, 255, 0)
        self.ORANGE = (255, 165, 0)
        self.PURPLE = (128, 0, 128)

        self.player_name: str   = "Player"
        self.player_speed: int  = 8
        self.ball_speed: int    = 5
        
        # Game state
        self.game_state: str = "main_menu"

        # Game options, add game options here
        self.option_to_gamestate: Dict[str, str] = {
            "START GAME": "start_game",
            "JOIN GAME" : "join_game",
            "SETTINGS"  : "settings",
            "EXIT"      : "exit",
            "MAIN MENU" : "main_menu"
        }
        self.gamestate_to_option: Dict[str, str] = {v: k for k, v in self.option_to_gamestate.items()}
        


        # Game options
        self.options: List[str] =  list(self.option_to_gamestate.keys()) # Get the options from the dictionary
        self.selected_option: int = 0 # The selected option at the moment, 0 is the first option
        self.font_options = pygame.font.Font(None, 40)
        
        
        # Network
        self.ip_address: str = ""        
        self.connection_established: bool = False
        self.network_thread:  Optional[threading.Thread] = None
        self.network: Network = None
        
        # Invalid game state button
        self.invalid_state_button_rect = pygame.Rect(20, self.window_height - 70, 200, 50)
        self.invalid_state_button_text = self.font_options.render("<- Back to Main Menu", True, self.WHITE)
        

        # Input rectangles for settings
        self.fixed_length = 200

        # The settings options are stored in a list of SettingData objects
        # To add a new setting, add a new SettingData object to the list, input and safe are the names of the input and safe variables
        self.settings_data: List[SettingData] = [
            SettingData(rect=None, safe="player_name"  , input="player_name_input"   , text="Player Name: "   , input_type="str"      , upper_limit=15    , lower_limit=1   ),
            SettingData(rect=None, safe="window_width" , input="window_width_input"  , text="Window Width: "  , input_type="int"      , upper_limit=1920  , lower_limit=400 ),
            SettingData(rect=None, safe="window_height", input="window_height_input" , text="Window Height: " , input_type="int"      , upper_limit=1080  , lower_limit=400 ),
            SettingData(rect=None, safe="ball_speed"   , input="ball_speed_input"    , text="Ball Speed: "    , input_type="int"      , upper_limit=20    , lower_limit=1   ),
            SettingData(rect=None, safe="player_speed" , input="player_speed_input"  , text="Player Speed: "  , input_type="int"      , upper_limit=20    , lower_limit=1   )
        ]
        self.reset_settings_input() # Reset the inputs to the values at the moment
        
    def get_gamestate_from_option(self, option: str) -> Optional[str]:
        """
        Get the gamestate from the option
        Args:
            option (str): The option to get the gamestate from

        Returns:
            str: The gamestate
        """
        
        return self.option_to_gamestate.get(option)

    def get_option_from_gamestate(self, gamestate: str) -> Optional[str]:
        """
        Get the option from the gamestate

        Args:
            gamestate (str): The gamestate to get the option from

        Returns:
            str: The option
        """
        
        return self.gamestate_to_option.get(gamestate)
        

    def run(self):

        while True:
            ret = self.render_screen()
            if ret is not None:
                return ret
            ret = self.handle_input()
            if ret is not None:
                return ret
            self.clock.tick(60)
            

    def render_screen(self) -> Optional[Network]:
        self.window.fill(self.BLACK) # Fill the screen with black

        
        if self.game_state == "main_menu":
            font_title = pygame.font.Font(None, 80)  # Increase font size for "Pong"
            title_text = font_title.render("Pong", True, self.WHITE)
            title_rect = title_text.get_rect(center=(self.window_width // 2, 100))
            
            # Render the options, except for the "MAIN MENU" option
            self.option_texts = [self.font_options.render(option, True, self.WHITE) for option in self.options if option != "MAIN MENU"]

            self.option_rects = [
                option_text.get_rect(center=(self.window_width // 2, self.window_height // 2 + index * 50))
                for index, option_text in enumerate(self.option_texts)
            ]

            self.window.blit(title_text, title_rect) # Draw the title text

            for index, option_rect in enumerate(self.option_rects):
                if option_rect.collidepoint(pygame.mouse.get_pos()):
                    self.selected_option = index
                    pygame.draw.rect(self.window, self.BLACK, option_rect.inflate(6, 6)) # Draw a black rectangle around the option
                else:
                    pygame.draw.rect(self.window, self.BLACK, option_rect) # Draw a black rectangle around the option

                if index == self.selected_option: # If the option is selected
                    selected_option_react = option_rect
                    # Draw underline for hovered option
                    underline_rect = pygame.Rect(selected_option_react.left, selected_option_react.bottom - 4,
                                                selected_option_react.width, 4)
                    pygame.draw.rect(self.window, self.WHITE, underline_rect) # Draw a white rectangle under the option

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
            
        elif self.game_state == "settings":
            self.render_settings()
            
        else:  # Other game states (including the error state)
            font_error = pygame.font.Font(None, 40)
            error_text = font_error.render(f"Invalid game state: \"{self.game_state}\"", True, self.RED)
            error_rect = error_text.get_rect(center=(self.window_width // 2, self.window_height // 2))

            # Render the error message
            self.window.blit(error_text, error_rect)

            # Render the "Back to Main Menu" button
            pygame.draw.rect(self.window, self.GRAY, self.invalid_state_button_rect)
            pygame.draw.rect(self.window, self.BLACK, self.invalid_state_button_rect.inflate(6, 6))
            self.window.blit(self.invalid_state_button_text, self.invalid_state_button_rect.move(10, 10))
            
        pygame.display.flip()
        return None    


    def handle_input(self)-> Optional[Network]:
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
                            self.switch_to_gamestate_from_option(self.options[self.selected_option])
                            # Add code for selected option action
                
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_pos = pygame.mouse.get_pos()
                    for index, option_rect in enumerate(self.option_rects):
                        if option_rect.collidepoint(mouse_pos):
                            self.selected_option = index
                            print(f"Option {self.selected_option + 1} selected")
                            self.switch_to_gamestate_from_option(self.options[self.selected_option])
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
            
            elif self.game_state == "settings":
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.save_button_rect.collidepoint(mouse_pos):
                        self.save_settings()
                        
                    else: 
                        for data in self.settings_data:
                            if data.rect.collidepoint(mouse_pos):
                                self.handle_setting_input(data.rect, data.input, type=data.input_type)
                                break
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game_state = "main_menu"

            else:   # Other game states (including the error state)
                if event.type == pygame.MOUSEBUTTONUP:
                    if self.invalid_state_button_rect.collidepoint(event.pos):
                        self.game_state = "main_menu"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                            self.game_state = "main_menu"
                    
        return None


    def switch_to_gamestate_from_option(self, option: str) -> None:
        """
        Switches to the selected option:
        - start_game: creates a server and waits for a connection, then starts the game
        - join_game: allows the user to enter an IP address to connect to
        - settings: allows the user to change the game settings
        - exit: exits the game 
        
        Args:
            option (str): The selected option
        """
        match_found:bool = True
        option_to_state: str = self.get_gamestate_from_option(option)
        
        match option_to_state:
            case "start_game":
                self.network_thread = threading.Thread(target=self.wait_for_connection)
                self.network_thread.start()
            case "join_game":
                pass
            case "settings":
                self.reset_settings_input()
            case "exit":
                pygame.quit()
                sys.exit()
            case _:
                #match_found = False # to stop from going to invalid states
                pass
        if match_found:
            self.game_state = option_to_state
            
    def wait_for_connection(self) -> None:
        self.network = Network(is_server=True, start_now=False)
        self.ip_address = self.network.start_socket()

        self.network.accept_connection()
        self.connection_established = True

    def handle_setting_input(self, input_rect: pygame.Rect, attribute_name: str, type: str = "int"):
        """
        handel the input of a setting

        Args:
            input_rect (pygame.Rect): the input rect on the screen
            attribute_name (str): the name where its gettings saved
            type (str): the type of the input ("int" or "str")
        """
        pygame.event.clear()

        active: bool = True
        while active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        active = False
                        continue
                        
                    match type:
                        case "int":
                            if event.key == pygame.K_BACKSPACE:
                                if len(str(getattr(self, attribute_name))) == 1:
                                    setattr(self, attribute_name, 0)
                                else:
                                    setattr(self, attribute_name, int(str(getattr(self, attribute_name))[:-1]))
                            elif event.key in [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5,
                                        pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                                digit = int(event.unicode)
                                setattr(self, attribute_name, int(str(getattr(self, attribute_name)) + str(digit)))
                                
                        case "str":
                            if event.key == pygame.K_BACKSPACE:
                                setattr(self, attribute_name, getattr(self, attribute_name)[:-1])
                            else:
                                if len(getattr(self, attribute_name)) < 15:  # Limit the input length if needed
                                    setattr(self, attribute_name, getattr(self, attribute_name) + event.unicode)
                
                elif event.type == pygame.MOUSEBUTTONUP:
                    mouse_pos = pygame.mouse.get_pos()
                    if not input_rect.collidepoint(mouse_pos):
                        active = False

            
            self.window.fill(self.BLACK)
            
            self.render_settings()
            pygame.draw.rect(self.window, self.YELLOW, input_rect, 2) # Highlight the active input field
            pygame.display.flip()
            self.clock.tick(60)

    def render_settings(self):
        font_settings = pygame.font.Font(None, 40)
        settings_text = font_settings.render("Settings", True, self.WHITE)
        settings_rect = settings_text.get_rect(center=(self.window_width // 2, self.window_height // 2 - 250))
        self.window.blit(settings_text, settings_rect)

        label_width: int = self.window_width // 2 - 250 # Width of the labels
        input_width: int = self.window_width // 2 - 50  # Width of the input fields
        
        font_input = pygame.font.Font(None, 32)

        for i, data in enumerate(self.settings_data):
            label = font_input.render(data.text, True, self.WHITE)
            label_rect = label.get_rect(midleft=(label_width, self.window_height // 2 - 150 + (50 * i)))
            input = font_input.render(str(getattr(self, data.input)), True, self.WHITE)
            input_height: int = self.window_height // 2 - 150 + (i * 50) - input.get_height()//2
            
            data.rect = pygame.Rect(input_width, input_height - 5, self.fixed_length, input.get_height() + 5)
            pygame.draw.rect(self.window, self.WHITE, data.rect, 2)
            
            self.window.blit(label, label_rect)
            self.window.blit(input, (input_width + 5, input_height))
            
            
        # Render the save button
        self.save_button_rect = pygame.Rect(self.window_width // 2 - 100, self.window_height - 100, 200, 50)
        save_button_text = font_input.render("Save Changes", True, self.WHITE)

        pygame.draw.rect(self.window, self.GRAY, self.save_button_rect)
        pygame.draw.rect(self.window, self.BLACK, self.save_button_rect.inflate(6, 6))
        self.window.blit(save_button_text, self.save_button_rect.move(10, 10))
            
        return
            
    def save_settings(self):
        print("Saving settings...")
        
        update_window: bool = False
        for data in self.settings_data:
            input = getattr(self, data.input)   # Get the input value
            value = getattr(self, data.safe)    # Get the current value

            if data.input_type == "int":
                # Check if the input is different from the current value and if its in the range
                if input != value and input > data.lower_limit and input < data.upper_limit:
                    setattr(self, data.safe, input)
                    if data.safe == "window_width" or data.safe == "window_height":
                        # If the window size is changed, the window needs to be resized
                        update_window = True

            elif data.input_type == "str":
                # Check if the input is different from the current value and if the length is in the range
                if input != value and len(input) > data.lower_limit and len(input) < data.upper_limit:
                    setattr(self, data.safe, input)  
                          
        if update_window is True:
            print("resizing window")
            self.window = pygame.display.set_mode((self.window_width, self.window_height))
            
    def reset_settings_input(self):
        
        for data in self.settings_data:
            setattr(self, data.input, getattr(self, data.safe))
            