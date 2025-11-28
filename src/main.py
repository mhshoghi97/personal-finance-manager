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
            show_balance(transactions)
            pass
        elif choice == "2":
            # Show Transactions
            show_transactions(transactions)
            pass
        elif choice == "3":
            # Add Transaction
            add_transaction(transactions)
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
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f" {len(data)} transactions loaded from {DATA_FILE}.")
                return data
        except (json.JSONDecodeError, Exception) as e:
            print("Error in loading data from JSON file. Please try again.")
            return []
    else:
        print("Data file not found.")
        return []

# Save transaction to the file
def save_data(transactions):
    """Save transactions to JSON file"""
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(transactions,f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error in saving transactions: {e}")

def add_transaction(transactions):
    """Add new transaction"""
    print("\n--- Add new transaction ---")


    # Get transaction type
    transaction_type = get_transaction_type()
    if transaction_type is None:
        return

    # Get amount
    transaction_amount = get_amount()
    if transaction_amount is None:
        return

    # Get category
    category = input("What category do you want to add? (Food, transportation, etc").strip()

    # Get description
    description = input("What description do you want to add? (optional)").strip()

    # Get date
    date = get_date()

    # Create new transaction
    transaction = {
        "id": len(transactions) + 1,
        "type": transaction_type,
        "amount": transaction_amount,
        "category": category,
        "description": description,
        "date": date,
    }


    # Append/Save transaction
    transactions.append(transaction)
    save_data(transactions)

def get_transaction_type():
    """Get transaction type from user"""
    while True:
        print("Transaction type: ")
        print("1. income")
        print("2. expense")
        choice = input("Choose your desired input: (1 or 2)").strip()

        if choice == "1":
            return "income"
        elif choice == "2":
            return "expense"
        elif choice.lower() == "exit":
            return None
        else:
            print("Invalid input. Only 1 or 2, (or exit)")

def get_amount():
    """Get amount from user"""
    while True:
        try:
            amount_input = input("Amount: ").strip()
            if amount_input.lower() == "exit":
                return None

            amount = float(amount_input)
            if amount <= 0:
                print("Amount must be greater than 0.")
                continue

            return amount

        except ValueError:
            print("Enter a valid amount. or (exit)")

def get_date():
    """Get date from user"""
    while True:
        date_input = input("Enter date or Press Enter for today's date: ").strip()

        if date_input == "":
            return datetime.now().strftime("%Y/%m/%d")

        else:
            try:
                # Date validation
                datetime.strptime(date_input, "%Y/%m/%d")
                return date_input
            except ValueError:
                print("❌ Invalid date format. Use YYYY/MM/DD (e.g., 2019-02-01)")

def show_balance(transactions):
    """Show current balance"""
    if not transactions:
        print("No transactions found.")
        return

    total_income = sum(t["amount"] for t in transactions if t["type"] == "income")
    total_expense = sum(t["amount"] for t in transactions if t["type"] == "expense")

    balance = total_income - total_expense


    print("\n--- Finance statistics: ---")
    print(f"Total Income: {total_income} $")
    print(f"Total Expense: {total_expense} $")
    print(f"Balance: {balance} $")


    if balance > 0:
        print("🎉 Your financial status is positive")
    elif balance < 0:
        print("⚠️ Your financial status is negative")
    else:
        print("⚖️ Your balance is zero.")

def show_transactions(transactions):
    """Show transactions"""
    if not transactions:
        print("No transaction found.")
        return

    print(f"\n{'ID':<4} {'Date':<12} {'Type':<8} {'Category':<15} {'Amount':<12} {'Description'}")
    print("-" * 70)

    for t in transactions:
        type_str = "income" if t["type"] == "income" else "expense"
        amount_str = f"{t['amount']:,.0f} $"
        print(f"{t['id']:<4} {t['date']:<12} {type_str:<8} {t['category']:<15} {amount_str:<12} {t['description']}")

if __name__ == "__main__":
    main()

