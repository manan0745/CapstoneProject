import json
import matplotlib.pyplot as plt

class FinanceTracker:
    def __init__(upes, filename="finance_data.json"):
        upes.filename = filename
        upes.transactions = upes.load_data()

    def load_data(upes):
        try:
            with open(upes.filename, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_data(upes):
        with open(upes.filename, "w") as file:
            json.dump(upes.transactions, file, indent=4)

    def add_transaction(upes, amount, category, transaction_type):
        transaction = {
            "amount": amount,
            "category": category,
            "type": "credit" if transaction_type == "i" else "debit"  
        }
        upes.transactions.append(transaction)
        upes.save_data()

    def view_transactions(upes):
        if not upes.transactions:
            print("\nNo transactions recorded.")
            return
        print("\nTransaction History:")
        for idx, t in enumerate(upes.transactions, 1):
            print(f"{idx}. {t['type'].capitalize()} - Rs{t['amount']} (Category: {t['category']})")

    def get_summary(upes):
        credit = sum(t["amount"] for t in upes.transactions if t["type"] == "credit") 
        debit = sum(t["amount"] for t in upes.transactions if t["type"] == "debit")  
        balance = credit - debit  

        print("\nSummary:")
        print(f"Total Credit: Rs{credit}")  
        print(f"Total Debit: Rs{debit}")  
        print(f"Remaining Balance: Rs{balance}")
        upes.show_pie_chart(credit, debit)  

    def show_pie_chart(upes, credit, debit):  
        labels = ['Credit', 'Debit']  
        amounts = [credit, debit]  
        plt.pie(amounts, labels=labels, autopct='%1.1f%%', startangle=90)
        plt.title("Credit vs Debit")  
        plt.axis('equal')
        plt.show()

    def category_breakdown(upes):
        debit_categories = {}
        for t in upes.transactions:
            if t["type"] == "debit":  
                cat = t["category"]
                debit_categories[cat] = debit_categories.get(cat, 0) + t["amount"]

        if not debit_categories:
            print("\nNo debit data to display.")  
            return

        print("\nDebit Category Breakdown:")  
        for cat, amt in debit_categories.items():
            print(f"- {cat.capitalize()}: Rs{amt}")

        plt.pie(debit_categories.values(), labels=debit_categories.keys(), autopct='%1.1f%%', startangle=140)
        plt.title("Debits by Category")  
        plt.axis('equal')
        plt.show()


print("🤗 Welcome to the Personal Finance Tracker🤗 \n")
tracker = FinanceTracker()

while True:
    print("\nMenu:")
    print("1. Add Transaction")
    print("2. View Transactions")
    print("3. View Summary")
    print("4. View Debit Categories")
    print("5. Exit")
    choice = input("Choose an option (1-5): ")

    if choice == "1":
        transaction_type = input("Enter transaction type (credit-C / debit-D): ").lower()  
        if transaction_type not in ["i", "d"]:  
            print("🙅🏻 Invalid transaction type.")
            continue
        try:
            amount = float(input("Enter the amount: Rs"))
            if amount < 0:
                raise ValueError
        except ValueError:
            print("🙅🏻Invalid amount. Please enter a positive number.")
            continue
        category = input("Enter the category (e.g., salary, groceries, rent): ").strip()
        tracker.add_transaction(amount, category, transaction_type)
        print("💁🏻‍♂️ Transaction added successfully.")

    elif choice == "2":
        tracker.view_transactions()

    elif choice == "3":
        tracker.get_summary()

    elif choice == "4":
        tracker.category_breakdown()

    elif choice == "5":
        print("🙋🏻‍♂️Exiting the Finance Tracker. Goodbye!")
        break

    else:
        print("🙅🏻  Invalid choice, please try again.")
