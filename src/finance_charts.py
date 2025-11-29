import numpy as np
from matplotlib import rcParams

try:
    import matplotlib.pyplot as plt
    import matplotlib.font_manager as fm
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False


class FinanceCharts:
    """Charts Management Class"""

    def __init__(self):
        pass

    def check_matplotlib(self):
        """Check matplotlib library installation."""
        if not HAS_MATPLOTLIB:
            print("The matplotlib library is not installed. Install it.")
            print("pip install matplotlib")
            return False
        return True

    def show_charts_menu(self, transactions):
        """Show charts menu"""
        if not self.check_matplotlib():
            return

        if not transactions:
            print("No transaction found!")
            return

        while True:
            print("\n--- Financial charts ---")
            print("1. Expense circular charts")
            print("2. Income vs. Expense Comparison ")
            print("4. Back to main menu")


            choice = input("Choose your input: ")

            if choice == "1":
                self.plot_expense_pie_chart(transactions)
            if choice == "2":
                self.plot_income_vs_expense(transactions)
            elif choice == "4":
                break
            else:
                print("Invalid input")

    def plot_expense_pie_chart(self, transactions):
        """Plot Expense Pie"""
        expense_by_category = {}
        for transaction in transactions:
            if transaction['type'] == 'expense':
                expense_by_category[transaction['category']] = expense_by_category.get(transaction['category'], 0) + transaction['amount']


        self._create_pie_chart(
            expense_by_category,
            "Distribution expenses by category",
            "red"
        )

    def plot_income_vs_expense(self, transactions):
        """Comparison between income and expense"""
        monthly_data = {}
        for t in transactions:
            year_month = t['date'][:7]
            if year_month not in monthly_data:
                monthly_data[year_month] = {'income': 0, 'expense': 0}

            if t['type'] == 'income':
                monthly_data[year_month]['income'] += t['amount']
            else:
                monthly_data[year_month]['expense'] += t['amount']

        if not monthly_data:
            print("No monthly data found")
            return

        months = sorted(monthly_data.keys())
        incomes = [monthly_data[m]['income'] for m in months]
        expenses = [monthly_data[m]['expense'] for m in months]

        plt.figure(figsize=(12, 6))
        x = np.arange(len(months))

        plt.bar(x - 0.2, incomes, width=0.4, label="Income", color="green", alpha=0.7)
        plt.bar(x + 0.2, expenses, width=0.4, label="Expense", color="red", alpha=0.7)

        plt.xlabel("Month")
        plt.ylabel("Amount ($)")
        plt.title("Comparison between income and expenses in different months")

        plt.xticks(x, months, rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.show()

    def _create_pie_chart(self, data, title, color_scheme):
        """ایجاد نمودار دایره‌ای"""
        categories = list(data.keys())
        amounts = list(data.values())

        # ایجاد طیف رنگی
        if color_scheme == 'green':
            colors = plt.cm.Greens(np.linspace(0.5, 0.8, len(categories)))
        else:
            colors = plt.cm.Reds(np.linspace(0.5, 0.8, len(categories)))

        plt.figure(figsize=(12, 8))
        patches, texts, autotexts = plt.pie(
            amounts,
            labels=categories,
            autopct='%1.1f%%',
            startangle=90,
            colors=colors,
            textprops={'fontsize': 12}
        )

        # بهبود نمایش اعداد و متن
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')

        plt.title(title, fontsize=16, fontweight='bold', pad=20)
        plt.axis('equal')
        plt.tight_layout()
        plt.show()


def create_chart_manager():
    return FinanceCharts()