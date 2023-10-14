from abc import ABC, abstractmethod

class Account(ABC):
    accounts = []
    total_balance = 0
    total_loan_amount = 0
    loan_enabled = True

    def __init__(self, name, email, address, account_type):
        self.name = name
        self.email = email
        self.address = address
        self.account_number = len(Account.accounts) + 1
        self.account_type = account_type
        self.balance = 0
        self.loan_count = 0
        Account.accounts.append(self)
        print(f"Account for {self.name} created successfully. Your account number is: {self.account_number}")

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            Account.total_balance += amount
            print(f"Deposited ${amount}. New balance: ${self.balance}")
        else:
            print("Invalid deposit amount")

    def withdraw(self, amount):
        if amount > 0:
            if self.balance >= amount:
                self.balance -= amount
                Account.total_balance -= amount
                print(f"Withdrew ${amount}. New balance: ${self.balance}")
            else:
                print("Withdrawal amount exceeded.")
        else:
            print("Invalid withdrawal amount")

    def check_balance(self):
        print(f"Available balance: ${self.balance}")

    def check_transaction_history(self):
        print("Transaction History:")
        for transaction in self.transactions:
            print(transaction)

    def take_loan(self, amount):
        if Account.loan_enabled and self.loan_count < 2:
            if amount > 0:
                self.balance += amount
                Account.total_loan_amount += amount
                self.loan_count += 1
                print(f"Loan of ${amount} taken. New balance: ${self.balance}")
            else:
                print("Invalid loan amount")
        else:
            print("Unable to take a loan at this time.")

    def transfer(self, recipient, amount):
        if recipient in Account.accounts:
            if self.balance >= amount:
                self.withdraw(amount)
                recipient.deposit(amount)
                print(f"Transferred ${amount} to {recipient.name}.")
            else:
                print("Insufficient balance to transfer.")
        else:
            print("Recipient account does not exist.")

    @abstractmethod
    def show_info(self):
        pass

    def __str__(self):
        return f"Account No: {self.account_number}, Name: {self.name}, Type: {self.account_type}"

class SavingsAccount(Account):
    def __init__(self, name, email, address):
        super().__init__(name, email, address, "Savings")

    def show_info(self):
        print(f"Account Information for {self.name}:")
        print(f"Account Type: {self.account_type}")
        print(f"Account Number: {self.account_number}")
        print(f"Current Balance: ${self.balance}")

class CurrentAccount(Account):
    def __init__(self, name, email, address):
        super().__init__(name, email, address, "Current")

    def show_info(self):
        print(f"Account Information for {self.name}:")
        print(f"Account Type: {self.account_type}")
        print(f"Account Number: {self.account_number}")
        print(f"Current Balance: ${self.balance}")

# Admin class
class Admin:
    def __init__(self, password):
        self.password = password

    def verify_password(self, input_password):
        return input_password == self.password

    def create_account(self, name, email, address, account_type):
        if account_type == "Savings":
            account = SavingsAccount(name, email, address)
        elif account_type == "Current":
            account = CurrentAccount(name, email, address)
        else:
            print("Invalid account type. Choose 'Savings' or 'Current'.")

    def delete_account(self, account):
        if account in Account.accounts:
            Account.accounts.remove(account)
            print(f"Account for {account.name} deleted.")
        else:
            print("Account not found.")

    def see_all_accounts(self):
        print("List of all accounts:")
        for account in Account.accounts:
            print(account)

    def check_total_balance(self):
        print(f"Total available balance in the bank: ${Account.total_balance}")

    def check_total_loan_amount(self):
        print(f"Total loan amount in the bank: ${Account.total_loan_amount}")

    def toggle_loan_feature(self, enable):
        Account.loan_enabled = enable
        status = "enabled" if enable else "disabled"
        print(f"Loan feature is {status}.")

# Main program
admin_password = '1234'
admin = Admin(admin_password)

while True:
    print("\nBanking Management System")
    print("1. User Operations")
    print("2. Admin Operations")
    print("3. Exit")
    choice = input("Choose an option (1/2/3): ")

    if choice == "1":
        # User Operations
        account_number = input("Enter your account number or '0' to go back to the main menu: ")
        if account_number == "0":
            continue
        for account in Account.accounts:
            if str(account.account_number) == account_number:
                user = account
                while True:
                    print(f"Welcome, {user.name}!")
                    print("1. Deposit")
                    print("2. Withdraw")
                    print("3. Check Balance")
                    print("4. Take Loan")
                    print("5. Transfer Money")
                    print("6. Logout")
                    option = input("Choose an option (1/2/3/4/5/6): ")
                    if option == "1":
                        amount = float(input("Enter the amount to deposit: $"))
                        user.deposit(amount)
                    elif option == "2":
                        amount = float(input("Enter the amount to withdraw: $"))
                        user.withdraw(amount)
                    elif option == "3":
                        user.check_balance()
                    elif option == "4":
                        amount = float(input("Enter the loan amount: $"))
                        user.take_loan(amount)
                    elif option == "5":
                        recipient_account_number = input("Enter the recipient's account number: ")
                        amount = float(input("Enter the amount to transfer: $"))
                        for recipient in Account.accounts:
                            if str(recipient.account_number) == recipient_account_number:
                                user.transfer(recipient, amount)
                                break
                        else:
                            print("Recipient account does not exist.")
                    elif option == "6":
                        break
                    else:
                        print("Invalid option. Please try again.")
                break
        else:
            print("Account not found. Please enter a valid account number.")

    elif choice == "2":
        # Admin Operations
        entered_password = input("Enter the admin password: ")
        if admin.verify_password(entered_password):
            print("Admin Operations:")
            print("1. Create Account")
            print("2. Delete Account")
            print("3. See All Accounts")
            print("4. Check Total Balance")
            print("5. Check Total Loan Amount")
            print("6. Toggle Loan Feature")
            print("7. Logout")
            admin_option = input("Choose an admin option (1/2/3/4/5/6/7): ")
            if admin_option == "1":
                name = input("Enter the name of the account holder: ")
                email = input("Enter the email: ")
                address = input("Enter the address: ")
                account_type = input("Enter the account type (Savings/Current): ")
                admin.create_account(name, email, address, account_type)
            elif admin_option == "2":
                account_number = int(input("Enter the account number to delete: "))
                for account in Account.accounts:
                    if account.account_number == account_number:
                        admin.delete_account(account)
                        break
                else:
                    print("Account not found.")
            elif admin_option == "3":
                admin.see_all_accounts()
            elif admin_option == "4":
                admin.check_total_balance()
            elif admin_option == "5":
                admin.check_total_loan_amount()
            elif admin_option == "6":
                enable_loan = input("Enable or Disable Loan Feature (enable/disable): ")
                if enable_loan == "enable":
                    admin.toggle_loan_feature(True)
                elif enable_loan == "disable":
                    admin.toggle_loan_feature(False)
                else:
                    print("Invalid choice. Please enter 'enable' or 'disable'.")
            elif admin_option == "7":
                continue
            else:
                print("Invalid admin option. Please try again.")
        else:
            print("Incorrect admin password. Access denied.")

    elif choice == "3":
        print("Goodbye!")
        break

    else:
        print("Invalid choice. Please try again.")
