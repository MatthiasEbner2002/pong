import pygame
from game import Game
from network import Network

debug: bool = True

def ask_for_start_choice_and_creat_network():
    
    network: Network = None
    
    start_choice: int = 0
    while start_choice not in ["1", "2"]:
        start_choice = input("Choose '1' to start a game or '2' to join a game: ")
    
    if start_choice == "1":
        network = Network(is_server=True)
        print("Server IP address:", network.host)
        
    elif start_choice == "2":
        server_ip: str = input("Enter the server IP address: ")
        network = Network(is_server=False, server_ip=server_ip)
        
    return network
    

def main():
    pygame.init()
    
    screen_width, screen_height = 800, 600
    game: Game = None
    
    if debug:
        network = ask_for_start_choice_and_creat_network()
        
        if network is None:
            print("Invalid input. (network is None)")
            return
        
        game = Game(screen_width, screen_height, network)
        
    else:
        game = Game(screen_width, screen_height)
    
    if game is None:
        print("Game is None")
        return
    
    network: Network = game.run()
    network.close_connection() # close connection
    pygame.quit() # quit pygame

if __name__ == "__main__":
    main()
