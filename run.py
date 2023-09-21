import gspread
from google.oauth2.service_account import Credentials
import random

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

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

    player_name = input("Enter your name: ")
    print(f"Welcome to the game {player_name}.")

    print("You will now create you character.")

    # Check for a character name written with letters and max 20 long.
    while True:
        char_name = input("Enter a character name: ")
        
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
            char_str = int(input("Strength: "))
            char_sta = int(input("Stamina: "))
            char_cha = int(input("Charisma: "))

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

def main():
    set_player()


if __name__ == '__main__':
    main()