import json
import os
from datetime import datetime


# File for saving data
DATA_FILE = "financial_data.json"

def main():
    """Main function"""
    print("Welcome to the MhShoghi Financial Manager!")

    # Loading available data
    transactions = load_data()

    # Show main menu
    while True:
        # Show Main Menu
        show_main_menu()
        choice = input("Choose your desired input: ")


        if choice == "1":
            # Show Balance
            pass
        elif choice == "2":
            # Show Transactions
            pass
        elif choice == "3":
            # Add Transaction
            pass
        elif choice == "4":
            print("Thanks! App closed!")
            break
        else:
            print("Invalid input. Please try again.")

def show_main_menu():
    """Main menu"""
    print("\n" + "="*40)
    print("Personal Financial Manager")
    print("="*40)
    print("1. Show balance")
    print("2. Show transactions history")
    print("3. Add transaction")
    print("4. Exit")


def load_data():
    """Load data from JSON file"""

    # Note: return an empty list now, later will complete this function
    return []


if __name__ == "__main__":
    main()

