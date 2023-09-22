import gspread
from google.oauth2.service_account import Credentials
import random

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

# ANSI color codes
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
END_COLOR = '\033[0m'  # Reset color to default

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('rpg_p3')

def set_player():
    """
    Ask for the players name.
    Create a character with name and stats for Stamina, Strength and Charisma.
    """
    print("Please enter your name.")
    print("Just one name with one word.")

    player_name = input("Enter your name:\n")
    print(f"Welcome to the game {player_name}.")

    print("You will now create you character.")

    # Check for a character name written with letters and max 20 long.
    while True:
        char_name = input("Enter a character name:\n")
        
        if char_name.isalpha() and len(char_name) <= 20:
            char_name = char_name.capitalize()  # Make the first letter uppercase, if not.
            break
        else:
            print("Character name must contain only letters and be a maximum of 20 characters.")
    
    print("\nYou will now create stats for your character.")
    print("You have a total of 12 Character Points (CP) to distribute over Stamina, Strength, and Charisma.")

    cp = 12

    # Initialize stats as None to enter the loop
    char_str = None
    char_sta = None
    char_cha = None

    while True:
        try:
            # Ask for input for each stat
            char_str = int(input("Strength:\n"))
            char_sta = int(input("Stamina:\n"))
            char_cha = int(input("Charisma:\n"))

            # Check if the sum of the entered stats is less than or equal to "cp"
            if char_str + char_sta + char_cha <= cp:
                break  # Exit the loop if the input is valid
            else:
                print(f"Total Character Points exceed {cp}. Please reenter values.")
        except ValueError:
            print("Please enter numeric values only.")

    # Shoow valid values for char_str, char_sta, and char_cha to player
    print(f"Welcome to the world {char_name}! Your stats are:")
    print(f"Strength: {char_str}\nStamina: {char_sta}\nCharisma: {char_cha}")

    # Open the "player" sheet
    player_sheet = SHEET.worksheet('player')
    
    #character_data = [player_name, char_name, char_str, char_sta, char_cha]
    #player_sheet.update("A2:E2", [character_data])
    player_sheet.update_acell('A2', player_name)
    player_sheet.update_acell('B2', char_name)
    player_sheet.update_acell('C2', char_str)
    player_sheet.update_acell('D2', char_sta)
    player_sheet.update_acell('E2', char_cha)

def roll_t10_dice():
    """
    Simulate rolling a ten-sided dice.
    Returns a random integer between 1 and 10.
    """
    return random.randint(1, 10)

    # Example usage:
    result = roll_t10_dice()
    print(f"You rolled a {result}")

def get_story():
    """
    Get one value from the 'story' sheet in your Google Sheet.
    Mark column A with 'x' if column B has been collected.
    Return the collected value.
    """
    story_sheet = SHEET.worksheet('story')
    story_data = story_sheet.get_all_values()

    last_retrieved_index = 0

    while last_retrieved_index < len(story_data):
        row = story_data[last_retrieved_index]
        if row[0] == 'x':
            last_retrieved_index += 1
            continue  # Skip rows that have already been collected
        if row[1]:  # Check if column B has a value
            story_sheet.update_cell(last_retrieved_index + 1, 1, 'x')  # Mark column A with 'x'
            return row[1]

    return None  # Return None if all rows have been collected

def ask_to_continue():
    """
    Ask the player if they want to continue or quit.
    Returns True to continue or False to quit.
    """
    while True:
        choice = input("Do you want to continue (y) or quit (n)?\n").lower()
        if choice == 'y':
            return True
        elif choice == 'n':
            return False
        else:
            print("Invalid choice. Please enter 'y' to continue or 'n' to quit.")

def reset_or_save():
    """
    Ask the player if they want to reset the story or save and quit.
    Returns 'reset' to reset the story or 'save' to save and quit.
    """
    while True:
        choice = input("Do you want to reset the story (r) or save and quit (s)?\n").lower()
        if choice == 'r':
            return 'reset'
        elif choice == 's':
            return 'save'
        else:
            print("Invalid choice. Please enter 'r' to reset or 's' to save and quit.")

def reset_story():
    # Get all values from column A
    story_sheet = SHEET.worksheet('story')
    column_a_values = story_sheet.col_values(1)

    # Remove all 'x' values
    for i, value in enumerate(column_a_values):
        if value == 'x':
            story_sheet.update_cell(i + 1, 1, '')

    print("Story completely resetted.")

def end_now():
    while True:
        # Ask if the player wants to continue or quit
        if not ask_to_continue():
            # Ask if the player wants to reset or save
            choice = reset_or_save()
            if choice == 'reset':
                # Reset the story (remove 'x' from column A)
                reset_story()
            elif choice == 'save':
                # Save and quit the game
                exit()
            break  # Exit the game loop

def dice_roll():
    """
    Perform a dice roll and display the result.
    Then, depending on the result, print the corresponding row from the 'diceroll' sheet.
    """
    # Get the 'diceroll' sheet
    diceroll_sheet = SHEET.worksheet('diceroll')

    print("Do you want to roll the dice?")
    while True:
        choice = input("y/n:\n").lower()
        if choice == 'y':
            # Perform a dice roll (random 1-6)
            result = random.randint(1, 6)

            # Display the result of the dice roll
            print(f"Your rolled: {result}")

            # Determine which row to print based on the dice roll result
            if result in [1, 2]:
                row = diceroll_sheet.row_values(1)
            elif result in [3, 4]:
                row = diceroll_sheet.row_values(2)
            elif result in [5, 6]:
                row = diceroll_sheet.row_values(3)

            # Print the corresponding row
            for cell_value in row:
                print(YELLOW + cell_value + END_COLOR)
                break
            return
        elif choice == 'n':
            print("You chose not to roll the dice. Ending the game.")
            return False
        else:
            print("Invalid choice. Please enter 'y' to roll or 'n' to end the game.")

    

def main():
    set_player()
    while True:
        storyline = get_story()
        print(YELLOW + storyline + END_COLOR)
        
        # Check if the storyline ends with "Dice roll!"
        if storyline.endswith("Dice roll:"):
            dice_roll()  # Call the dice_roll function

        if not ask_to_continue():
            choice = reset_or_save()
            if choice == 'reset':
                reset_story()
                break  # Exit the game loop
            elif choice == 'save':
                break  # Exit the game loop
    print("Game saved. Goodbye!")

if __name__ == '__main__':
    main()