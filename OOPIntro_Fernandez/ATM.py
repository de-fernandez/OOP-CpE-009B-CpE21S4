"""
    ATM.py
"""

class ATM():
    def __init__(self, account, serial_number):
        self.account = account
        self.serial_number = serial_number
        self.transaction_history = []

    def deposit(self, account, amount):
        account.current_balance = account.current_balance + amount
        transaction = f"Deposited {amount} to account {account.account_number}. New Balance: {account.current_balance}"
        self.transaction_history.append(transaction)
        print("Deposite Complete")

    def widthdraw(self, account, amount):
        account.current_balance = account.current_balance - amount
        transaction = f"Withdrew {amount} from account {account.account_number}. New Balance: {account.current_balance}"
        self.transaction_history.append(transaction)
        print("Widthdraw Complete")

    def check_currentbalance(self, account):
        data = account.current_balance
        transaction = f"Checked a balance of {data} from account {account.account_number}."
        self.transaction_history.append(transaction)
        print(data)

    def view_transactionsummary(self):
        if not self.transaction_history:
            print("No Transaction.")
        else:
            print("Transaction Summary:")
            for transaction in self.transaction_history:
                print(transaction)