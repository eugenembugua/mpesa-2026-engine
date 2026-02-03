from abc import ABC, abstractmethod
import re

class Recipient(ABC):
    @abstractmethod
    def receive_funds(self, amount, sender_id, reference=None): pass

class Account:
    def __init__(self, owner_id, balance=0):
        self._owner_id = owner_id #Protected
        self.__balance = balance   #Private (Hidden)

    def get_balance(self):
        return self.__balance

    def update_balance(self, amount):
        self.__balance += amount
        return self.__balance

class User:
    def __init__(self, name, phone, balance=0):
        #Exactly 10 digits
        if not re.fullmatch(r'\d{10}', phone):
            raise ValueError("Invalid Phone: Must be exactly 10 digits (e.g., 0712345678).")
        
        self.__name = name 
        self._phone = phone
        self.account = Account(phone, balance)

    def get_full_name(self):
        return self.__name
    
    def get_masked_name(self):
        return f"{self.__name[0]}****{self.__name[-1]}"

class Business(Recipient):
    def __init__(self, id, name, type="Till"):
        self.id, self.name, self.type = id, name, type
    def receive_funds(self, amount, sender_id, reference=None):
        return f"Confirmed. {amount} paid to {self.name}."

class Tariff:
    #TRANSFER TO M-PESA USERS, POCHI, TILL, AND OTHER REGISTERED USERS
    TRANSFER_RANGES = [
        (1, 100, 0), (101, 500, 7), (501, 1000, 13), (1001, 1500, 23),
        (1501, 2500, 33), (2501, 3500, 53), (3501, 5000, 57), (5001, 7500, 78),
        (7501, 10000, 90), (10001, 15000, 100), (15001, 20000, 105), 
        (20001, 250000, 108)
    ]
    
    #WITHDRAWAL FROM M-PESA AGENT
    WITHDRAW_RANGES = [
        (50, 100, 11), (101, 2500, 29), (2501, 3500, 52), (3501, 5000, 69),
        (5001, 7500, 87), (7501, 10000, 115), (10001, 15000, 167),
        (15001, 20000, 185), (20001, 35000, 197), (35001, 50000, 278),
        (50001, 250000, 309)
    ]

    @classmethod
    def get_fee(cls, amount, category):
        #Category check based on your transaction types
        if category in ["Send Money", "Pochi", "Buy Goods", "Paybill", "Bank_Transfer"]:
            ranges = cls.TRANSFER_RANGES
        elif category == "Withdrawal":
            ranges = cls.WITHDRAW_RANGES
        else:
            return 0 # Airtime, Deposits, etc. are FREE

        for low, high, fee in ranges:
            if low <= amount <= high:
                return fee
        return 0