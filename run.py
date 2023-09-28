import gspread
from google.oauth2.service_account import Credentials
import random
from gspread.exceptions import SpreadsheetNotFound
import os
import sys

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
DEFAULT_COLOR = '\033[0m'  # Reset color to default

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)

"""
Error handling if Google sheet is not found
"""
try:
    GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
    SHEET = GSPREAD_CLIENT.open('rpg_p3')
except (Exception, SpreadsheetNotFound) as e:
    if isinstance(e, SpreadsheetNotFound):
        print("The 'rpg_p3' Google Sheet not found. Please make sure it exists.")
    else:
        print(f"Sorry, there was an error authorizing Google Sheets API: {e}")
    exit(1)

def set_player():
    """
    Ask for the player's name.
    Create a char with a name and stats for Stamina, Strength, and Charisma.
    """
    print("To start, would you please tell us who you are?")

    while True:
        player_name = input("Enter your name:\n")
        if player_name.isalpha() and len(player_name) <= 20:
            player_name = player_name.capitalize()  # Set first letter to uppercase.
            break
        else:
            print("Your name must have only letters and be a max 20 characters.")

    print(GREEN + f"Welcome to the game {player_name}." + DEFAULT_COLOR)

    print("Time to create your character.")

    # Check if character name is written with letters and max 20 characters.
    while True:
        char_name = input("Enter a character name:\n")

        player_sheet = SHEET.worksheet('player')
        existing_char_name_value = player_sheet.acell('B2')
        
        # Get any existing character name from google sheet.
        existing_char_name = existing_char_name_value.value.strip() if existing_char_name_value.value else None

        if char_name.isalpha() and len(char_name) <= 20:
            char_name = char_name.capitalize()
            if existing_char_name is not None and char_name == existing_char_name:
                print("Character already exists. Continuing the story...")
                return False
            else:
                print("New character in progress...")
                reset_story()  # Reset the story if new character name is entered.
            break
        else:
            print("Name must contain letters only and be a maximum of 20 characters.")

        
    print("\nYou will now create stats for your character.")

    cp = 12 # Character Points (cp) to distribute over stats.

    print(f"You have a total of {cp} Character Points to \ndistribute over Strength, Stamina, and Charisma.")

    char_str = None
    char_sta = None
    char_cha = None

    while True:
        try:
            # Ask for input for stats.
            char_str = int(input("Strength:\n"))
            char_sta = int(input("Stamina:\n"))
            char_cha = int(input("Charisma:\n"))

            # Check if the sum of the stats is less than or equal to "cp".
            if char_str + char_sta + char_cha <= cp:
                break  # Exit the loop if the input is valid.
            else:
                print(f"Total Character Points exceed {cp}. Reenter values.")
        except ValueError:
            print("Please enter numeric values only.")

    # Shoow valid values for char_str, char_sta, and char_cha to player
    print(f"Welcome to the world {char_name}! Your stats are:")
    print(f"Strength: {char_str}\nStamina: {char_sta}\nCharisma: {char_cha}")
    print("Game starting...")

    # Open the "player" sheet
    player_sheet = SHEET.worksheet('player')
    player_sheet.update_acell('A2', player_name)
    player_sheet.update_acell('B2', char_name)
    player_sheet.update_acell('C2', char_str)
    player_sheet.update_acell('D2', char_sta)
    player_sheet.update_acell('E2', char_cha)

def get_story():
    """
    Get text from the story sheet from Google Sheet.
    Mark row in col A with "x" if col B has been used.
    """
    story_sheet = SHEET.worksheet('story')
    story_data = story_sheet.get_all_values()

    last_retrieved_index = 0

    while last_retrieved_index < len(story_data):
        row = story_data[last_retrieved_index]
        if row[0] == 'x':
            last_retrieved_index += 1
            continue  # Skip rows that have already been used.
        if row[1]:  # Check if column B has a value.
            # If, mark column A with 'x'
            story_sheet.update_cell(last_retrieved_index + 1, 1, 'x')  
            return row[1]

    return None  # Return None if story ended.

def roll_dice_and_display(char_stat, message):
    """
    Perform a dice roll and display the result.
    """
    while True:
        choice = input("Do you want to roll the dice? (y/n):\n").lower()
        if choice == 'y':
            # Perform a dice roll (random 1-6)
            dice_value = random.randint(1, 6)

            # Check if the character stat value is not None
            if char_stat is not None:
                try:
                    # Convert the character stat value to an integer
                    char_stat_value = int(char_stat)
                except ValueError:
                    print(f"Error: The value is not a valid integer: {char_stat}")
                    return False
            else:
                print("Error: The value is None. Are the character stats set?")
                return False

            # Calculate the result
            result = (dice_value + char_stat_value) / 2

            # Display the result of the dice roll
            print(BLUE + f"{message} {dice_value}" + DEFAULT_COLOR)
            print(BLUE + f"Your dice roll combined with your character's stats gives you the power of {result}" + DEFAULT_COLOR)

            return result
        elif choice == 'n':
            print("You chose not to roll the dice. Ending the game.")
            return False
        else:
            print("Invalid choice. Please enter 'y' to roll or 'n' to end the game.")

def ask_to_continue():
    """
    Ask the player if they want to continue or quit.
    Returns True to continue or False to quit.
    """
    while True:
        choice = input("Do you want to continue (c) or quit (q)?\n").lower()
        if choice == 'c':
            return True
        elif choice == 'q':
            return False
        else:
            print("Invalid choice. Please enter 'c' to continue or 'q' to quit.")

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
            print("Invalid choice.")
            print("Please enter 'r' to reset or 's' to save and quit.")

def reset_story():
    # Remove all "x" values from the "story" sheet
    story_sheet = SHEET.worksheet('story')
    column_a_values = story_sheet.col_values(1)
    
    for i, value in enumerate(column_a_values):
        if value == 'x':
            story_sheet.update_cell(i + 1, 1, '')

    # Clear row 2 in the "player" sheet
    SHEET.worksheet('player').delete_rows(2)
    # Reset the dice roll trigger to 1.
    SHEET.worksheet('diceroll').update_acell('C1', 1)

    print("Story resetted.")
    

def end_now():
    while True:
        # Ask if the player wants to continue or quit.
        if not ask_to_continue():
            # Ask if the player wants to reset or save.
            choice = reset_or_save()
            if choice == 'reset':
                # Reset game (remove "x" from column A)
                reset_story()
                break
            elif choice == 'save':
                break

def dice_roll_fight():
    """
    Perform a dice roll and display the result.
    Then, depending on the result,
    print the corresponding row from the 'diceroll' sheet.
    """
    char_str_value = SHEET.worksheet('player').acell('C2').value
    message = "With a roll of the dice combined with your strength, you invoke a surge\nof luck and chance. The dice dance through the air,\nand as it land, it reveal the outcome:"
    result = roll_dice_and_display(char_str_value, message)
    
    row = []  # Initialize row

    if result is not False:
        # Get the "diceroll" sheet
        diceroll_sheet = SHEET.worksheet('diceroll')
        
        # Decides which row to print based on the dice roll result.
        if 0 <= result < 4:
            row = diceroll_sheet.row_values(2)
        elif 4 <= result < 7:
            row = diceroll_sheet.row_values(3)
        elif 7 <= result:
            row = diceroll_sheet.row_values(4)

        # Print the corresponding row
        for cell_value in row:
            print(YELLOW + cell_value + DEFAULT_COLOR)
            break

def dice_roll_journey():
    """
    Perform a dice roll and display the result.
    Then, depending on the result of the dice roll combined with
    strength and stamina, print the corresponding row from the 'diceroll' sheet.
    """
    char_sta_value = SHEET.worksheet('player').acell('D2').value
    message = "With a roll of the dice combined with your stamina, you invoke a surge\nof luck and chance. The dice dance through the air,\nand as it land, it reveal the outcome:"
    result = roll_dice_and_display(char_sta_value, message)
    row = []

    if result is not False:
        # Connect the "diceroll" sheet.
        diceroll_sheet = SHEET.worksheet('diceroll')

        # Decides which row to print based on the dice roll result.
        if 0 <= result < 4:
            row = diceroll_sheet.row_values(6)
        elif 4 <= result < 7:
            row = diceroll_sheet.row_values(7)
        elif 7 <= result:
            row = diceroll_sheet.row_values(8)

        # Print the corresponding row.
        for cell_value in row:
            print(YELLOW + cell_value + DEFAULT_COLOR)
            break

def dice_roll_meeting():
    """
    Perform a dice roll and display the result.
    Then, depending on the result of the dice roll combined with charisma,
    print the corresponding row from the 'diceroll' sheet.
    """
    char_cha_value = SHEET.worksheet('player').acell('E2').value
    message = "With a roll of the dice combined with your charisma, you invoke a surge\nof luck and chance. The dice dance through the air,\nand as it land, it reveal the outcome:"
    result = roll_dice_and_display(char_cha_value, message)
    row = []

    if result is not False:
        # Get the "diceroll" sheet
        diceroll_sheet = SHEET.worksheet('diceroll')

        # Decides which row to print based on the dice roll result.
        if 0 <= result < 4:
            row = diceroll_sheet.row_values(10)
        elif 4 <= result < 7:
            row = diceroll_sheet.row_values(11)
        elif 7 <= result:
            row = diceroll_sheet.row_values(12)

        # Print the right row.
        for cell_value in row:
            print(YELLOW + cell_value + DEFAULT_COLOR)
            break

def main():
    """
    Main game function to handle "game mechanics".
    """
    set_player()
    
    while True:
        storyline = get_story()
        trigger = int(SHEET.worksheet('diceroll').acell('C1').value)
        
        if storyline is not None:
            print(YELLOW + storyline + DEFAULT_COLOR)

            # Check if the storyline says it's time to roll dice.
            if storyline.endswith("Time to roll your dice:") and trigger == 1:
                dice_roll_fight()
                SHEET.worksheet('diceroll').update_acell('C1', 2)

            elif storyline.endswith("Time to roll your dice:") and trigger == 2:
                dice_roll_journey()
                SHEET.worksheet('diceroll').update_acell('C1', 3)

            elif storyline.endswith("Time to roll your dice:") and trigger == 3:
                dice_roll_meeting()
                SHEET.worksheet('diceroll').update_acell('C1', 1)
            
            if not ask_to_continue():
                choice = reset_or_save()
                if choice == 'reset':
                    # Resetting story (remove "x" from column A).
                    reset_story()
                    break
                elif choice == 'save':
                    break
        else:
            reset_story()
            break

    print(f"Thank you for playing. Goodbye!\n")
    print(RED + f"Rebooting game...\n" + DEFAULT_COLOR)

    # Restart game
    python = sys.executable
    os.execl(python, python, *sys.argv)

if __name__ == '__main__':
    main()