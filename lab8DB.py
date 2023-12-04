from sqlalchemy import create_engine, Column, Integer, Float, String, ForeignKey, func
from sqlalchemy.orm import declarative_base, Session, relationship
from datetime import datetime

engine = create_engine('sqlite:///bank.db', echo=False)
Base = declarative_base()

class BankAccount(Base):
    __tablename__ = 'BankAccounts'

    Id = Column(Integer, primary_key=True)
    AccountNumber = Column(String, unique=True)
    Balance = Column(Float, default=0.0)
    Transactions = relationship("Transaction", back_populates="Account")

class Transaction(Base):
    __tablename__ = 'Transactions'

    Id = Column(Integer, primary_key=True)
    Amount = Column(Float)
    Description = Column(String)
    Date = Column(String)
    AccountId = Column(Integer, ForeignKey('BankAccounts.Id'))
    Account = relationship("BankAccount", back_populates="Transactions")

Base.metadata.create_all(engine)

def create_session():
    return Session(engine)

def create_account(session, account_number):
    new_account = BankAccount(AccountNumber=account_number)
    session.add(new_account)
    session.commit()

def deposit(session, account_number, amount, description):
    account = session.query(BankAccount).filter_by(AccountNumber=account_number).first()
    if account:
        transaction = Transaction(Amount=amount, Description=description, Date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        account.Balance += amount
        account.Transactions.append(transaction)
        session.commit()

def withdraw(session, account_number, amount, description):
    account = session.query(BankAccount).filter_by(AccountNumber=account_number).first()
    if account and account.Balance >= amount:
        transaction = Transaction(Amount=-amount, Description=description, Date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        account.Balance -= amount
        account.Transactions.append(transaction)
        session.commit()

def get_balance(session, account_number):
    account = session.query(BankAccount).filter_by(AccountNumber=account_number).first()
    return account.Balance if account else None

def get_transactions(session, account_number):
    account = session.query(BankAccount).filter_by(AccountNumber=account_number).first()
    return account.Transactions if account else []

def close_session(session):
    session.close()

# Приклад використання
session = create_session()

# Створити банківський акаунт
create_account(session, "248239235")

# Здійснити операції
deposit(session, "248239235", 1000.0, "Deposit")
withdraw(session, "248239235", 500.0, "Withdraw")

# Отримати баланс та транзакції
balance = get_balance(session, "248239235")
print(f"Balance: {balance}")

transactions = get_transactions(session, "248239235")
print("Transactions:")
for transaction in transactions:
    print(f"{transaction.Date} | {transaction.Description} | {transaction.Amount}")

# Закрити сесію
close_session(session)
