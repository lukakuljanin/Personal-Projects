import os
from simple_colors import * 

ships = {'Carrier': 5, 'Battleship': 4, 'Cruiser': 3, 'Submarine': 3, 'Destroyer': 2}



# Prints out the player's board depending on the turn
def print_board(player, board_1, board_2):
    os.system('cls' if os.name == 'nt' else 'clear')
    
    current_board = board_1 if player == 1 else board_2
    print(magenta(f"Player {player}'s Board\n", ['bold', 'underlined']))
    
    # Prints letters on left of board and numbers at the bottom
    for i, row in enumerate(current_board):
        print(magenta(chr(i + 65)), ' '.join(colour_tile(tile) for tile in row))
    print('  ' + ' '.join(str(magenta(i + 1)) for i in range(10)) + '\n')



def place_phase(player, board_1, board_2):

    current_board = board_1 if player == 1 else board_2

    while ships:
        print_board(player, board_1, board_2)
        
        print(green('Available ships:'))
        for name, size in ships.items():
            print(f"{name}: {size}")
        
        print(green('\nControls:'))
        print("Format: [length][row][column][direction]")
        print("Examples: 5A1R (Carrier at A1 going right), 3B10L (Cruiser at B10 going left)")
        print("Directions: R = right, L = left, U = up, D = down")
        
        code = input("\nEnter code (or 'x' to reset, 'xxx' to quit): ")
        
        if code.lower() == 'x':
            ships = {'Carrier': 5, 'Battleship': 4, 'Cruiser': 3, 'Submarine': 3, 'Destroyer': 2}
            # Clear the board
            current_board = [['-' for i in range(10)] for j in range(10)]
            print(yellow("\nAll ships removed!"))
            input("\nPress Enter to continue...")
        
        elif code.lower() == 'xxx':
            print('\nBye! Thanks for playing!\n')
            exit()