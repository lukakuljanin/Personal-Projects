import os
from simple_colors import * 

colours = {'-': blue, '■': green, 'X': red}

# Colours the board tiles depending on the item
def colour_tile(tile):
    return colours.get(tile, lambda x: x)(tile)

# Makes a 10 by 10 board
def make_board():
    return [['-' for i in range(10)] for j in range(10)]

# Takes in errors list and prints them
def print_errors(errors):
    for i in errors:
        print(red(f"\n{i}"))

    input(yellow("\nPress 'ENTER' to continue: "))

# Prints out the player's board
def print_board(player, current_board):
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(magenta(f"Player {player}'s Board\n", ['bold', 'underlined']))
    
    # Prints letters on left of board and numbers at the bottom
    for i, row in enumerate(current_board):
        print(magenta(chr(i + 65)), ' '.join(colour_tile(tile) for tile in row))
    print('  ' + ' '.join(str(magenta(i + 1)) for i in range(10)) + '\n')



def battle_phase(player_1_board, player_2_board, player_1_attack_board, player_2_attack_board):
    player = 2

    while True:
        current_attack_board = player_1_attack_board if player == 2 else player_2_attack_board
        player = 1 if player == 2 else 2

        while True:
            print_board(current_attack_board)

            print(green("\nControls:"))
            print("Format: [letter][number]")
            print("Examples: A5, B10")

            coord = input(yellow("Enter the coordinate you would like to attack (or 'xxx' to quit): "))

            # Quit game
            if coord.lower() == 'xxx':
                print("\nBye! Thanks for playing!\n")
                exit()


            if len(coord) in range(2, 4):
                try:
                    letter = coord[0].upper()
            
                    # Handle both single and double digit numbers 
                    number = int(coord[1]) if len(coord) == 2 else int(coord[1:3])
                
                except (ValueError, IndexError):
                    print(red("\nInvalid format. Must be letter + number (ex. A5 or B10)"))

            else:
                print(red("\nInvalid format. Coordinate must be 2-3 characters long (ex. A5 or B10)"))
            




        



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
        
        code = input(yellow("\nEnter code (or 'x' to reset board, 'xxx' to quit): "))
    
        # Reset ship placements
        if code.lower() == 'x':
            ships = {'Carrier': 5, 'Battleship': 4, 'Cruiser': 3, 'Submarine': 3, 'Destroyer': 2}
            current_board = [['-' for i in range(10)] for j in range(10)]
            print(yellow("\nAll ships removed!"))
            input(yellow("\nPress 'ENTER' to continue: "))
            continue
    
        # Quit game
        elif code.lower() == 'xxx':
            print("\nBye! Thanks for playing!\n")
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
                print(red("\nInvalid format. Code must be length + letter + number + direction (ex. 5A1D or 4B10D)"))
    
            errors = []

            # Validate ship length exists in available ships
            if length not in ships.values():
                errors.append(f"Invalid ship length. Available lengths: {set(ships.values())}")
    
            # Validate letter (A-J)
            if letter not in "ABCDEFGHIJ":
                errors.append("Row must be a letter from A-J")
    
            # Validate number (1-10)
            if number not in range(1, 11):
                errors.append("Column must be an integer from 1-10")
    
            # Validate direction
            if direction not in "RLUD":
                errors.append("Direction must be R (right), L (left), U (up), or D (down)")
            

            # Print errors if any
            if errors:
                print_errors(errors)


            # If code format is valid, check if ship placement is valid
            else:
                # Change letter and number into row and column
                row = ord(letter) - 65
                col = number - 1
                coords = []
                
                # Get coords for ship placement
                for i in range(length):
                    if direction == 'R':
                        coords.append((row, col + i))
                    elif direction == 'L':
                        coords.append((row, col - i))
                    elif direction == 'D':
                        coords.append((row + i, col))
                    elif direction == 'U':
                        coords.append((row - i, col))


                # Check if ship placement is in bounds
                for row, col in coords:
                    # Check if invalid placement
                    if row < 0 or row >= 10 or col < 0 or col >= 10:
                        # Append error if detected
                        errors.append("Ship would be placed out of bounds")
                        break


                # Check if ship placement is adjacent to other ships
                found_adjacent_ship = False

                # Check if invalid placement
                for row, col in coords:
                    # Break if adjacent ships were found 
                    if found_adjacent_ship:
                        break

                    # Check all 8 surrounding tiles using dr and dc
                    for delta_row in [-1, 0, 1]:
                        # Break if adjacent ships were found
                        if found_adjacent_ship:
                            break
                            
                        for delta_col in [-1, 0, 1]:
                            # Skip current tile
                            if delta_row == 0 and delta_col == 0:
                                continue
                            
                            check_row, check_col = row + delta_row, col + delta_col
                            
                            # Check if adjacent position is in bounds
                            if 0 <= check_row < 10 and 0 <= check_col < 10:
                                # If adjacent tile has a ship and is not part of the ship being placed
                                if current_board[check_row][check_col] == '■' and (check_row, check_col) not in coords:
                                    # Raise flag error
                                    found_adjacent_ship = True
                                    break
                
                # Append error if detected
                if found_adjacent_ship:
                    errors.append("Ship must be at least one tile away from other ships")


                # Print errors if any
                if errors:
                    print_errors(errors) 

                # If ship placement is valid
                else:
                    # Place ship on board
                    for row, col in coords:
                        current_board[row][col] = '■'

                    # Remove ship from ships dictionary
                    for ship_name, ship_size in list(ships.items()):
                        if ship_size == length:
                            del ships[ship_name]
                            break

                    # Check if it was the last ship
                    if not len(ships):
                        print_board(player, current_board)
                        print("All ships placed!")
                        confirm = input(yellow("\nAre you satisfied with your ship placement? (y/n): "))
                            
                        if confirm.lower() == 'y':
                            print(green("\nShip placement confirmed!"))
                            input(yellow("\nPress 'ENTER' to continue: "))
                            break

                        else:
                            # Reset ships and board for the player
                            ships = {'Carrier': 5, 'Battleship': 4, 'Cruiser': 3, 'Submarine': 3, 'Destroyer': 2}
                            current_board = [['-' for i in range(10)] for j in range(10)]
                            print("\nResetting your board, place your ships again!")
                            input(yellow("\nPress 'ENTER' to continue: "))


        # If code isn't correct length
        else:
            print(red("\nInvalid format. Code must be 4-5 characters long (ex. 5A1D or 4B10D)"))



# Main function that starts the game
def start_game():
    player_1_board = make_board()
    player_2_board = make_board()

    player_1_attack_board = make_board()
    player_2_attack_board = make_board()
    
    place_phase(1, player_1_board)
    place_phase(2, player_2_board)

    battle_phase()


start_game()