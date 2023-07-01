import pygame
from game import Game
from network import Network

def main():
    pygame.init()
    screen_width, screen_height = 800, 600
    debug: bool = False
    
    if debug:
        start_choice = input("Choose '1' to start a game or '2' to join a game: ")
        if start_choice == "1":
            network = Network(is_server=True)
            print("Server IP address:", network.host)
        elif start_choice == "2":
            server_ip = input("Enter the server IP address: ")
            network = Network(is_server=False, server_ip=server_ip)

        game = Game(screen_width, screen_height, network)
        
    else:
        game = Game(screen_width, screen_height)
    network: Network = game.run()
    network.close_connection()
    pygame.quit()

if __name__ == "__main__":
    main()
