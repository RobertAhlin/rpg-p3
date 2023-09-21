import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('rpg_p3')

def set_player_name():
    """
    Ask for the players name.
    """
    print("Please enter your name.")
    print("Just one name with one word.")

    player_name_str = input("Enter your name: ")
    print(f"Welcome to the game {player_name_str}.")

set_player_name()