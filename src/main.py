import json
import os
from datetime import datetime
from finance_charts import create_chart_manager


# File for saving data
DATA_FILE = "financial_data.json"

def main():
    """Main function"""
    print("Welcome to the MhShoghi Financial Manager!")


    chart_manager = create_chart_manager()

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
        elif choice == "2":
            # Show Transactions
            show_transactions(transactions)
        elif choice == "3":
            # Add Transaction
            add_transaction(transactions)
        elif choice == "4":
            # Edit Transaction
            edit_transactions(transactions)
        elif choice == "5":
            # Delete Transaction
            delete_transaction(transactions)
        elif choice == "6":
            # Search Transaction
            search_transactions(transactions)
        elif choice == "7":
            # Financial Reports
            show_financial_reports(transactions)
        elif choice == "9":
            chart_manager.show_charts_menu(transactions)
        elif choice == "11":
            print("\n Thanks. Your data saved!")
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
    print("4. Edit transactions")
    print("5. Delete transaction")
    print("6. Search transactions")
    print("7. Statistics and Reports")

    print("9. Financial charts")
    # Others
    print("8. Exit the program")

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
    category = input(f"What category do you want to add? (Food, transportation, etc) = ").strip()

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

def edit_transactions(transactions):
    """Edit an available transaction"""
    if not transactions:
        print("No transaction found.")
        return

    # Show transactions list
    show_transactions(transactions)

    try:
        transaction_id = int(input("\nChoice your transaction ID: "))
    except ValueError:
        print("Enter a valid transaction ID.")
        return

    # Find the transaction
    transaction = find_transaction_by_id(transactions, transaction_id)
    if not transaction:
        print(f"Transaction with ID {transaction_id} not found")
        return

    print(f"\nEdit transaction {transaction['id']:<4}")
    print(f"Balance: {transaction['amount']} - {transaction['type']} - {transaction['category']:<12}")

    # Show edit menu
    while True:
        print("\nWhat field would you like to edit?")
        print("1. Transaction Type")
        print("2. Amount")
        print("3. Category")
        print("4. Description")
        print("5. Date")
        print("6. Save + Exit")

        field_choice = input("Choose your desired input: (1 or 6)").strip()


        if field_choice == "1":
            new_type = get_transaction_type()
            if new_type:
                transaction["type"] = new_type
                print("✅ Transaction type updated and set to " + new_type)

        elif field_choice == "2":
            new_amount = get_amount()
            if new_amount:
                transaction["amount"] = new_amount
                print("✅ Transaction amount updated and set to " + str(new_amount))


        elif field_choice == "3":
            new_category = input("New category: ").strip()
            if new_category:
                transaction["category"] = new_category
                print("✅ Transaction category updated.")

        elif field_choice == "4":
            print("*" * 40)
            print("You are editing description for transaction ID: ")
            print(f"Balance: {transaction['amount']} - {transaction['type']} - {transaction['category']:<12}")
            new_description = input("New description: ").strip()
            transaction["description"] = new_description
            print("✅ Transaction description updated.")

        elif field_choice == "5":
            new_date = get_date()
            if new_date:
                transaction["date"] = new_date
                print("✅ Transaction date updated.")

        elif field_choice == "6":
            save_data(transactions)
            print("✅ Changes saved.")
            break
        else:
            print("❌ Invalid input field")

# Find transaction By ID
def find_transaction_by_id(transactions, transaction_id):
    """Find transaction by id"""
    for t in transactions:
        if t["id"] == transaction_id:
            return t

    return None

def delete_transaction(transactions):
    """Delete transaction"""
    if not transactions:
        print("No transaction found.")
        return

    show_transactions(transactions)

    try:
        transaction_id = int(input("\nChoice your transaction ID: "))
    except ValueError:
        print("Enter a valid transaction ID.")
        return


    # Find transaction
    transaction = find_transaction_by_id(transactions, transaction_id)
    if not transaction:
        print(f"Transaction with ID {transaction_id} not found")


    # Display transaction
    print(f"\nAre you sure you want to delete {transaction['id']}?")
    type_str = "income" if transaction["type"] == "income" else "expense"
    print(f" {type_str} - {transaction['category']} - {transaction['amount']:,.0f} $ - {transaction['description']}")

    confirm = input("Type 'yes' for confirmation (y/n): ").strip()

    if confirm == "yes":
        transactions.remove(transaction)

        # Update ids
        for i, transaction in enumerate(transactions, start=1):
            transaction['id'] = 1
        save_data(transactions)

        print("Transaction deleted successfully.")
    else:
        print("Aborted.")

def search_transactions(transactions):
    """Search transactions by input"""
    if not transactions:
        print("No transaction found.")
        return


    # Define fields
    print("\n--- Search in transactions ---")
    print("1. 🔍 Search based on category")
    print("2. 📅 Search based on date")
    print("3. 💰 Search based on transaction type")
    print("4. 🔎 Search in description")


    # choice field input
    choice = input("Choose your desired input: (1 or 4)")

    if choice == "1":
        # Search by category
        search_by_category(transactions)
    elif choice == "2":
        # Search by date
        search_by_date(transactions)
    elif choice == "3":
        # Search by type
        search_by_type(transactions)
    elif choice == "4":
        # Search in description
        search_by_description(transactions)
    else:
        print("Invalid input")
        return

def search_by_category(transactions):
    """Search transactions by category"""
    category = input("Your category: ").strip().lower()
    if not category:
        print("Category should not be empty.")
        return

    results = [t for t in transactions if category in t['category'].lower()]
    show_search_results(results, f"Show results for category '{category}'")

def search_by_date(transactions):
    """Search transactions by date"""
    date = input("Date: (YYYY/MM/DD): ").strip()
    if not date:
        print("Date should not be empty.")
        return

    try:
        datetime.strptime(date, "%Y-%m-%d")
        results = [t for t in transactions if t['date'] == date]
        show_search_results(results, f"Show results for date '{date}'")

    except ValueError:
        print("Invalid date")

def search_by_type(transactions):
    """Search transactions by type"""
    print("\nTransaction Type:")
    print("1. Income")
    print("2. Expense")

    choice = input("Choose 1 or 2:")
    if choice == "1":
        results = [t for t in transactions if t['type'] == 'income']
        show_search_results(results, f"Show results for type 'income'")

    elif choice == "2":
        results = [t for t in transactions if t['type'] == 'expense']
        show_search_results(results, f"Show results for type 'expense'")
    else:
        print("Invalid input")

def search_by_description(transactions):
    """Search transactions by description"""
    keyword = input("Keyword: ").strip().lower()
    if not keyword:
        print("Keyword should not be empty.")
        return
    results = [t for t in transactions if keyword in t['description'].lower()]
    show_search_results(results, f"Show results for keyword '{keyword}'")

def show_search_results(results, title):
    """Show search results"""
    if not results:
        print(f"No search results found.")
        return

    print(f"\n--- {title} ---")
    print(f" {len(results)} search results found.")
    print(f"{'ID':<4} {'Date':<12} {'type':<8} {'category':<15} {'amount':<15} {'description':<15}")
    print("-" * 70)

    for r in results:
        type_str = "income" if r["type"] == "income" else "expense"
        amount_str = f"{r['amount']:,.0f} $"
        print(f"{r['id']:<4} {r['date']:<12} {r['type']:<8} {r['category']:<15}  {amount_str:<15} {r['description']:<15}")

def show_financial_reports(transactions):
    """Show financial reports"""
    if not transactions:
        print("No transaction found for financial reports.")
        return

    while True:
        print("\n--- Financial reports ---")
        print("1. 📋 Summary")
        print("2. 🏷️ Statistics based on category")
        print("3. 📅 Monthly report")
        print("4. 🔙 Main Menu")

        choice = input("Choose your desired input: (1 or 4)").strip()

        if choice == "1":
            # Summary
            show_summary_report(transactions)
            pass
        elif choice == "2":
            # category report
            show_category_report(transactions)
        elif choice == "3":
            # monthly report
            show_monthly_report(transactions)
        elif choice == "4":
            break
        else:
            print("Invalid input")

def show_summary_report(transactions):
    """Show summary report"""
    total_income = sum(t['amount'] for t in transactions if t['type'] == 'income')
    total_expense = sum(t['amount'] for t in transactions if t['type'] == 'expense')
    balance = total_income - total_expense

    # income_count = len([t for t in transactions if t['type'] == 'income'])
    # Update (for better usage and performance)
    income_count = len([t for t in transactions if t['type'] == 'income'])
    expense_count = len([t for t in transactions if t['type'] == 'expense'])


    print("\n--- 📋 Overall Financial Summary ---")
    print(f"💰 Total income: {total_income:,.0f} $ ({income_count} transactions)")
    print(f"💸 Total Expenses: {total_expense:,.0f} $ ({expense_count} transactions)")
    print(f"💳 Final Balance: {balance:,.0f} $")

    if total_income > 0:
        savings_ratio = ((total_income - total_expense) / total_income) * 100
        print(f"🎯 Rate of savings: {savings_ratio:.2f}%")

def show_category_report(transactions):
    """Show category report"""
    # Grouping income by category
    income_by_category = {}
    for t in transactions:
        if t['type'] == 'income':
            income_by_category[t['category']] = income_by_category.get(t['category'],0) + t['amount']

    # Grouping expense by category
    expense_by_category = {}
    for t in transactions:
        if t['type'] == 'expense':
            expense_by_category[t['category']] = expense_by_category.get(t['category'], 0) + t['amount']

    print("\n--- Statistics based on category ---")

    if income_by_category:
        print("\n Income by category")
        for category, amount in sorted(income_by_category.items(), key=lambda x: x[1], reverse=True):
            percentage = (amount / sum(income_by_category.values())) * 100
            print(f"{category}: {amount:,.0f} ({percentage:.2f}%)")

    if expense_by_category:
        print("\n Expenses by category")
        for category, amount in sorted(expense_by_category.items(), key=lambda x: x[1], reverse=True):
            percentage = (amount / sum(expense_by_category.values())) * 100
            print(f"{category}: {amount:,.0f} ({percentage:.2f}%)")

def show_monthly_report(transactions):
    """Show monthly report"""

    # Define an empty dictionary
    monthly_data = {}
    for t in transactions:
        year_month = t['date'][:7] # YYYY-MM

        if year_month not in monthly_data:
            monthly_data[year_month] = {'income': 0, 'expense': 0 }

        if t['type'] == 'income':
            monthly_data[year_month]['income'] += t['amount']
        else:
            monthly_data[year_month]['expense'] += t['amount']

    if not monthly_data:
        print("No monthly data found.")
        return

    print("\n--- Monthly Report ---")
    for month, data in sorted(monthly_data.items()):
        balance = data['income'] - data['expense']
        print(f"\n {month}")
        print(f"Income: {data['income']:,.0f} $")
        print(f"Expense: {data['expense']:,.0f} $")
        print(f"Balance: {balance:,.0f} $")


if __name__ == "__main__":
    main()

