import os
from simple_colors import * 

colours = {'-': blue, '■': green, 'X': red}

# Colours the board tiles depending on the item
def colour_tile(tile):
    return colours.get(tile, lambda x: x)(tile)



# Prints out the player's board depending on the turn
def print_board(player, current_board):
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(magenta(f"Player {player}'s Board\n", ['bold', 'underlined']))
    
    # Prints letters on left of board and numbers at the bottom
    for i, row in enumerate(current_board):
        print(magenta(chr(i + 65)), ' '.join(colour_tile(tile) for tile in row))
    print('  ' + ' '.join(str(magenta(i + 1)) for i in range(10)) + '\n')





def place_phase(player, current_board):
    ships = {'Carrier': 5, 'Battleship': 4, 'Cruiser': 3, 'Submarine': 3, 'Destroyer': 2}

    while ships:
        print_board(player, current_board)
        
        print(green("Available ships:"))
        for name, size in ships.items():
            print(f"{name}: {size}")
        
        print(green("\nControls:"))
        print("Format: [length][row][column][direction]")
        print("Examples: 5A1R (Carrier at A1 going right), 3B10L (Cruiser at B10 going left)")
        print("Directions: R = right, L = left, U = up, D = down")
        
        while True:
            errors = []
            code = input("\nEnter code (or 'x' to reset board, 'xxx' to quit): ")
        
            if code.lower() == 'x':
                # Reset ships and clear board
                ships = {'Carrier': 5, 'Battleship': 4, 'Cruiser': 3, 'Submarine': 3, 'Destroyer': 2}
                current_board = [['-' for i in range(10)] for j in range(10)]
                print(yellow("\nAll ships removed!"))
                input("\nPress Enter to continue...")
                continue
        
            elif code.lower() == 'xxx':
                print('\nBye! Thanks for playing!\n')
                exit()


            # Validate the input code and returns parsed values or error message
            if len(code) in range(4, 6):
                try:
                    length = int(code[0])
                    letter = code[1].upper()
            
                    # Handle both single and double digit columns 
                    if len(code) == 4:
                        number = int(code[2])
                        direction = code[3].upper()
                    else:  # len(code) == 5
                        number = int(code[2:4])
                        direction = code[4].upper()
                
                except (ValueError, IndexError):
                    print("Invalid format. Use: length + letter + number + direction (ex. 5a1d or 5a10d)")
        
        
                # Validate ship length exists in available ships
                if length not in ships.values():
                    errors.append(f"Invalid ship length. Available lengths: {set(ships.values())}")
        
                # Validate letter (A-J)
                if letter not in "ABCDEFGHIJ":
                    errors.append("Row must be a letter from A-J")
        
                # Validate number (1-10)
                if number not in range(1, 11):
                    reerrors.append("Column must be an integer from 1-10")
        
                # Validate direction
                if direction not in "RLUD":
                    errors.append("Direction must be R (right), L (left), U (up), or D (down)")
                

                # Print errors if any
                if errors:
                    for i in errors:
                        print(red(f"\n{i}"))

                # If code is valid
                else:
                    for ship_name, ship_size in ships.items():
                        if ship_size == length:
                            del ships[ship_name]


                    # Check if this was the last ship
                    if not len(ships):
                        print_board(player, current_board)
                        print(yellow("\nAll ships placed!"))
                        confirm = input("\nAre you satisfied with your ship placement? (y/n): ")
                            
                        if confirm.lower() == 'y':
                            print(green("\nShip placement confirmed!"))
                            input("Press Enter to continue...")
                            break

                        else:
                            # Reset ships and board for this player
                            ships = {'Carrier': 5, 'Battleship': 4, 'Cruiser': 3, 'Submarine': 3, 'Destroyer': 2}
                            board_1 = [['-' for i in range(10)] for j in range(10)]
                            print(yellow("\nResetting your board. Place your ships again!"))
                            input("Press Enter to continue...")

            else:
                print("\nCode must be 4-5 characters long (ex. 5a1d or 5a10d)")




# Main function that starts the game
def start_game():
    board_1 = [['-' for i in range(10)] for j in range(10)]
    board_2 = [['0' for i in range(10)] for j in range(10)]
    
    place_phase(1, board_1)
    place_phase(2, board_2)


start_game()