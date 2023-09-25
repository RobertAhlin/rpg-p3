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
                print("Error: The value is None.")
                return False

            # Calculate the result
            result = (dice_value + char_stat_value) / 2

            # Display the result of the dice roll
            print(BLUE + f"{message} {dice_value}" + END_COLOR)
            print(BLUE + f"Your dice roll combined with your character's stat gives you the power of {result}" + END_COLOR)

            return result
        elif choice == 'n':
            print("You chose not to roll the dice. Ending the game.")
            return False
        else:
            print("Invalid choice. Please enter 'y' to roll or 'n' to end the game.")

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

        # Open the "player" sheet
        player_sheet = SHEET.worksheet('player')
        existing_char_name = player_sheet.acell('B2').value.strip()  # Get the existing character name and remove leading/trailing spaces
        
        if char_name == existing_char_name:
            print("Character already exist. Continuing the story...")
            return False
        else:
            print("New character in progress..")
            reset_story() # Reset story for a new character.
        if char_name.isalpha() and len(char_name) <= 20:
            char_name = char_name.capitalize()  # Make the first letter uppercase, if not.
            break
        else:
            print("Character name must contain only letters and be a maximum of 20 characters.")

    print("\nYou will now create stats for your character.")
    print("You have a total of 12 Character Points (CP) to distribute over Strength, Stamina, and Charisma.")

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
    print(f"Strength: {char_str}\nStamina: {char_sta}\nCharisma: {char_cha}\nGame starting...")

    # Open the "player" sheet
    player_sheet = SHEET.worksheet('player')
    
    # character_data = [player_name, char_name, char_str, char_sta, char_cha]
    # player_sheet.update("A2:E2", [character_data])
    player_sheet.update_acell('A2', player_name)
    player_sheet.update_acell('B2', char_name)
    player_sheet.update_acell('C2', char_str)
    player_sheet.update_acell('D2', char_sta)
    player_sheet.update_acell('E2', char_cha)

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
            print("Invalid choice. Please enter 'r' to reset or 's' to save and quit.")

def reset_story():
    # Get all values from column A
    story_sheet = SHEET.worksheet('story')
    column_a_values = story_sheet.col_values(1)

    # Remove all 'x' values
    for i, value in enumerate(column_a_values):
        if value == 'x':
            story_sheet.update_cell(i + 1, 1, '')

    print("Story completely reset.")

def end_now():
    while True:
        # Ask if the player wants to continue or quit
        if not ask_to_continue():
            # Ask if the player wants to reset or save
            choice = reset_or_save()
            if choice == 'reset':
                # Reset the story (remove 'x' from column A)
                reset_story()
                break  # Exit the game loop
            elif choice == 'save':
                break  # Exit the game loop

def dice_roll_fight():
    """
    Perform a dice roll and display the result.
    Then, depending on the result, print the corresponding row from the 'diceroll' sheet.
    """
    char_str_value = SHEET.worksheet('player').acell('C2').value
    message = "With a roll of the dice combined with your strength, you invoke a surge\nof luck and chance. The dice dance through the air,\nand as they land, they reveal their outcome:"
    result = roll_dice_and_display(char_str_value, message)
    
    if result is not False:
        # Get the 'diceroll' sheet
        diceroll_sheet = SHEET.worksheet('diceroll')
        
        # Determine which row to print based on the dice roll result
        if 1 <= result <= 3:
            row = diceroll_sheet.row_values(2)
        elif 4 <= result <= 6:
            row = diceroll_sheet.row_values(3)
        elif 7 <= result <= 9:
            row = diceroll_sheet.row_values(4)

        # Print the corresponding row
        for cell_value in row:
            print(YELLOW + cell_value + END_COLOR)
            break

def dice_roll_journey():
    """
    Perform a dice roll and display the result.
    Then, depending on the result of the dice roll combined with
    strength and stamina, print the corresponding row from the 'diceroll' sheet.
    """
    char_str_value = SHEET.worksheet('player').acell('C2').value
    char_sta_value = SHEET.worksheet('player').acell('D2').value
    message = "With a roll of the dice combined with your strength, you invoke a surge\nof luck and chance. The dice dance through the air,\nand as they land, they reveal their outcome:"
    result = roll_dice_and_display(char_str_value, message)

    if result is not False:
        # Get the 'diceroll' sheet
        diceroll_sheet = SHEET.worksheet('diceroll')

        # Determine which row to print based on the dice roll result
        if 0 <= result <= 3:
            row = diceroll_sheet.row_values(6)
        elif 4 <= result <= 6:
            row = diceroll_sheet.row_values(7)
        elif 7 <= result <= 9:
            row = diceroll_sheet.row_values(8)

        # Print the corresponding row
        for cell_value in row:
            print(YELLOW + cell_value + END_COLOR)
            break

def dice_roll_meeting():
    """
    Perform a dice roll and display the result.
    Then, depending on the result of the dice roll combined with charisma,
    print the corresponding row from the 'diceroll' sheet.
    """
    char_cha_value = SHEET.worksheet('player').acell('E2').value
    message = "With a roll of the dice combined with your charisma, you invoke a surge\nof luck and chance. The dice dance through the air,\nand as they land, they reveal their outcome:"
    result = roll_dice_and_display(char_cha_value, message)

    if result is not False:
        # Get the 'diceroll' sheet
        diceroll_sheet = SHEET.worksheet('diceroll')

        # Determine which row to print based on the dice roll result
        if 1 <= result <= 3:
            row = diceroll_sheet.row_values(10)
        elif 4 <= result <= 6:
            row = diceroll_sheet.row_values(11)
        elif 7 <= result <= 9:
            row = diceroll_sheet.row_values(12)

        # Print the corresponding row
        for cell_value in row:
            print(YELLOW + cell_value + END_COLOR)
            break

def main():
    set_player()
    while True:
        storyline = get_story()
        if storyline is not None:
            print(YELLOW + storyline + END_COLOR)

            # Check if the storyline ends with "a gift from the mischievous Forest Oracle."
            dice_roll_fight() if storyline.endswith("a gift from the mischievous Forest Oracle.") else None

            # Check if the storyline ends with "With a roll of the dice, you determine your fate."
            dice_roll_journey() if storyline.endswith("With a roll of the dice, you determine your fate.") else None

            # Check if the storyline ends with "with every word and gesture."
            dice_roll_meeting() if storyline.endswith("with every word and gesture.") else None

            if not ask_to_continue():
                choice = reset_or_save()
                if choice == 'reset':
                    # Reset the story (remove 'x' from column A)
                    reset_story()
                    break  # Exit the game loop
                elif choice == 'save':
                    break  # Exit the game loop
        else:
            break  # Exit the game loop
    print("Thank you for playing. Goodbye!")

if __name__ == '__main__':
    main()