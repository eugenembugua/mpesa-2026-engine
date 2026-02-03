from models import Tariff
import json
from datetime import datetime

class MPesaEngine:
    def __init__(self, logger, security, phonebook_path='hakikisha.json'):
        self.logger, self.security = logger, security
        self.phonebook_path = phonebook_path

    def _load_db(self):
        try:
            with open(self.phonebook_path, 'r') as f: return json.load(f)
        except FileNotFoundError: return {}

    def _save_db(self, data):
        with open(self.phonebook_path, 'w') as f: json.dump(data, f, indent=4)

    def get_recipient_name(self, identifier, category=None, store_id=None):
        db = self._load_db()
        identifier = str(identifier) 

        if category == "Personal":
            person = db.get("PERSONAL_CONTACTS", {}).get(identifier)
            if person: return person.get("name")
            
        elif category == "Agent":
            agent = db.get("AGENT_DIRECTORY", {}).get(identifier, {})
            name = agent.get('name', 'Unknown Agent')
            location = agent.get('location', 'Unknown Location')
            return f"{name} - {location}"
            
        elif category == "Business":
            biz = db.get("BUSINESS_DIRECTORY", {}).get(identifier)
            if biz: 
                return f"{biz.get('name')} - {biz.get('category')}"
            
        elif category == "Pochi":
            pochi = db.get("POCHI_DIRECTORY", {}).get(identifier)
            if pochi:  
                return f"{pochi.get('name')} - {pochi.get('business')}"
            
        elif category == "Crypto":
            wallet = db.get("CRYPTO_WALLETS", {}).get(identifier)
<<<<<<< HEAD
            if wallet:
                return f"{wallet.get('name')}"
=======
            if wallet: return wallet.get("name")
            return f"Wallet {identifier[:4]}..." 
>>>>>>> 90f26134e12423dae4455a9bd4164f27843b7d4c
        
        return identifier
        
    def show_preview(self, amount, txn_type, recipient_id, **kwargs):
        store_id = kwargs.get('store_id')
        acc_no = kwargs.get('acc_no')
        
<<<<<<< HEAD
        cat_map = {
            "Send Money": "Personal", "Withdrawal": "Agent", 
            "Paybill": "Business", "Buy Goods": "Business", 
            "Pochi": "Pochi", "Bank_Transfer": "Business",
            "Crypto_Buy": "Crypto"
        }
=======
        cat_map = {"Send Money": "Personal", "Withdrawal": "Agent", "Paybill": "Business", "Buy Goods": "Business", "Pochi": "Pochi"}
>>>>>>> 90f26134e12423dae4455a9bd4164f27843b7d4c
        name = self.get_recipient_name(recipient_id, category=cat_map.get(txn_type), store_id=store_id)
        
        fee = Tariff.get_fee(amount, txn_type)
        total = amount + fee
        
<<<<<<< HEAD
        print(f"\n\033[93m| TRANSACTION PREVIEW | (Hakikisha kabla ya kutuma)\033[0m")
=======
        print(f"\n\033[93m| TRANSACTION PREVIEW |(Hakikisha kabla ya kutuma)\033[0m")
>>>>>>> 90f26134e12423dae4455a9bd4164f27843b7d4c
        print(f"------------------------------------------")
        print(f"Service: {txn_type}")
        print(f"To:      {name}")
        if acc_no: print(f"Account: {acc_no}")
<<<<<<< HEAD
        print(f"Amount:  {amount:,.2f} KES")
        print(f"Fee:     {fee:,.2f} KES")
=======
        print(f"Amount:  {amount} KES")
        print(f"Fee:     {fee} KES")
>>>>>>> 90f26134e12423dae4455a9bd4164f27843b7d4c
        print(f"------------------------------------------")
        print(f"\033[1mTotal to be deducted: {total:,.2f} KES\033[0m")
        print(f"------------------------------------------")
        return total

    def _execute_transaction(self, user, recipient, amount, txn_type, pin, meta=None, tag="General"):
<<<<<<< HEAD
=======
        #Load current stats for Daily Limit
>>>>>>> 90f26134e12423dae4455a9bd4164f27843b7d4c
        data = self.security.load_secrets() 
        self.security.check_and_reset_limit(data) 

        incoming_types = ["Bank_Topup", "Crypto_Sell"]
        is_incoming = txn_type in incoming_types
        
<<<<<<< HEAD
        if not is_incoming and amount > 500000:
             print(f"\033[91m[!] Safety Block: {amount:,.2f} KES exceeds single transaction limits.\033[0m")
             return False

=======
        #To catch "fat-finger" crypto errors
        if not is_incoming and amount > 500000:
             print(f"\033[91m[!] Safety Block: {amount:,.2f} KES exceeds single transaction limits.\033[0m")
             print("Check if you entered coin units (e.g. 100 BTC) instead of KES.")
             return False

        #Daily Limit Enforcement (Outgoing only)
>>>>>>> 90f26134e12423dae4455a9bd4164f27843b7d4c
        if not is_incoming and not self.security.is_within_limit(amount, data):
            remaining = data["daily_limit"] - data["spent_today"]
            print(f"\033[91m[!] Limit Exceeded. You can only transact {remaining:,.2f} KES more today.\033[0m")
            return False

<<<<<<< HEAD
=======
        #Security & PIN Verification
>>>>>>> 90f26134e12423dae4455a9bd4164f27843b7d4c
        if not self.security.verify_pin(pin):
            return False
        
        fee = Tariff.get_fee(amount, txn_type)
        total_to_deduct = 0 if is_incoming else (amount + fee)
<<<<<<< HEAD
        b_before = user.account.get_balance()

        if is_incoming or b_before >= total_to_deduct:
            balance_change = amount if is_incoming else -total_to_deduct
            user.account.update_balance(balance_change)
=======
        
        #Capture BALANCE BEFORE
        b_before = user.account.get_balance()

        if is_incoming or b_before >= total_to_deduct:
            #Update Balance
            balance_change = amount if is_incoming else -total_to_deduct
            user.account.update_balance(balance_change)
            
            #Capture BALANCE AFTER
>>>>>>> 90f26134e12423dae4455a9bd4164f27843b7d4c
            b_after = user.account.get_balance()

            if not is_incoming:
                data["spent_today"] += amount 
            
            self.security.save_secrets(data) 
            
<<<<<<< HEAD
            now_dt = datetime.now()
            txn_id = self.logger.log_transaction(
                s=user._phone, r=recipient, t=txn_type, a=amount, f=fee, 
                b_before=b_before, b_after=b_after, tag=tag, meta=str(meta), timestamp=now_dt
            )
            
=======
            #Log to CSV 
            now_dt = datetime.now()
            txn_id = self.logger.log_transaction(
                s=user._phone, 
                r=recipient, 
                t=txn_type, 
                a=amount, 
                f=fee, 
                b_before=b_before, 
                b_after=b_after, 
                tag=tag,  # Tag is saved here for history
                meta=str(meta), 
                timestamp=now_dt
            )
            
            #Resolve recipient display name
>>>>>>> 90f26134e12423dae4455a9bd4164f27843b7d4c
            cat_map = {
                "Send Money": "Personal", "Withdrawal": "Agent", 
                "Paybill": "Business", "Buy Goods": "Business", 
                "Pochi": "Pochi", "Bank_Transfer": "Business",
                "Bank_Topup": "Business", "Crypto_Buy": "Crypto",      
                "Crypto_Sell": "Crypto", "Airtime": "Personal"
            }
            
            display_name = self.get_recipient_name(
                recipient, 
                category=cat_map.get(txn_type), 
<<<<<<< HEAD
                store_id=meta.get('store') if meta and 'store' in meta else None
            )

=======
                store_id=meta.get('store') if meta else None
            )

            #Build identification string for SMS
            receiver_identifier = ""
            if meta and 'acc' in meta:
                prefix = "from" if is_incoming else "to"
                receiver_identifier = f"{prefix} Acc. {meta['acc']}"
            elif meta and 'wallet' in meta:
                prefix = "from" if is_incoming else "to"
                receiver_identifier = f"{prefix} Wallet {meta['wallet']} ({meta.get('units')} {meta.get('asset')})"
            else:
                receiver_identifier = f"to {recipient}"
                
            #SMS Formatting
>>>>>>> 90f26134e12423dae4455a9bd4164f27843b7d4c
            date_sms = now_dt.strftime("%d/%m/%y")
            time_sms = now_dt.strftime("%I:%M %p")
            rem_limit = data["daily_limit"] - data["spent_today"]
            formatted_txn_id = f"{txn_id[:1]}-{txn_id[1:]}" if not txn_id.startswith("U-") else txn_id

<<<<<<< HEAD
            print(f"\n\033[92mM-PESA MESSAGE\033[0m")
            
            #CUSTOM CRYPTO SELL MESSAGE
            if txn_type == "Crypto_Sell":
                print(f"{formatted_txn_id} Confirmed. You have received Ksh{amount:,.2f} from {display_name} ")
                print(f"for the sale of {meta['units']:.8f} {meta['asset']} from {meta['account_name']} ")
                print(f"on {date_sms} at {time_sms}. New M-PESA balance is Ksh{b_after:,.2f}. ")

            #CUSTOM CRYPTO BUY MESSAG
            elif txn_type == "Crypto_Buy":
                #Extract the asset name from meta data to avoid NameError
                asset = meta.get('asset', 'Units') 
                print(f"{formatted_txn_id} Confirmed. Ksh{amount:,.2f} sent to {display_name} ")
                print(f"for {meta['units']:.8f} {asset} on {date_sms} at {time_sms}. ")
                print(f"New M-PESA balance is Ksh{b_after:,.2f}. Transaction cost, Ksh{fee:,.2f}.")
                print(f"\033[94m[{display_name.upper()} CREDITED]\033[0m")
                acc_name = meta.get('account_name', 'Wallet')
                print(f"Asset Worth: Ksh{amount:,.2f} added to {acc_name}.")
                
            elif is_incoming:
                print(f"{formatted_txn_id} Confirmed. You have received Ksh{amount:,.2f} from {display_name} ")
                print(f"on {date_sms} at {time_sms}. New M-PESA balance is Ksh{b_after:,.2f}. ")
            
            elif txn_type == "Withdrawal":
                print(f"{formatted_txn_id} Confirmed. Ksh{amount:,.2f} withdrawn from {display_name} ")
                print(f"on {date_sms} at {time_sms}. New M-PESA balance is Ksh{b_after:,.2f}. ")
                print(f"Withdrawal Charge Ksh{fee:,.2f}.")
                
            elif txn_type == "Airtime":
                print(f"{formatted_txn_id} Confirmed. Ksh{amount:,.2f} airtime purchased for {recipient} ")
                print(f"on {date_sms} at {time_sms}. New M-PESA balance is Ksh{b_after:,.2f}. ")
                print(f"Transaction cost, Ksh{fee:,.2f}.")
            
            else:
                print(f"{formatted_txn_id} Confirmed. Ksh{amount:,.2f} sent to {display_name} ")
                print(f"on {date_sms} at {time_sms}. New M-PESA balance is Ksh{b_after:,.2f}. ")
                print(f"Transaction cost, Ksh{fee:,.2f}. Amount you can transact within the day is {rem_limit:,.2f}. ")
            
            return True
=======
            #AUTHENTIC SMS OUTPUT
            print(f"\n\033[92mM-PESA MESSAGE\033[0m")
            
            if is_incoming:
                print(f"{formatted_txn_id} Confirmed. You have received Ksh{amount:,.2f} from {display_name} {receiver_identifier} "
                      f"on {date_sms} at {time_sms}. New M-PESA balance is Ksh{b_after:,.2f}. ")
            
            elif txn_type == "Withdrawal":
                print(f"{formatted_txn_id} Confirmed. Ksh{amount:,.2f} withdrawn from {display_name} "
                      f"on {date_sms} at {time_sms}. New M-PESA balance is Ksh{b_after:,.2f}. "
                      f"Withdrawal Charge Ksh{fee:,.2f}. To reverse, forward this message to 456.")
            
            elif txn_type == "Airtime":
                print(f"{formatted_txn_id} Confirmed. Ksh{amount:,.2f} airtime purchased for {recipient} "
                      f"on {date_sms} at {time_sms}. New M-PESA balance is Ksh{b_after:,.2f}. "
                      f"Transaction cost, Ksh{fee:,.2f}. To reverse, forward this message to 456.")
            
            else:
                print(f"{formatted_txn_id} Confirmed. Ksh{amount:,.2f} sent to {display_name} "
                      f"on {date_sms} at {time_sms}. New M-PESA balance is Ksh{b_after:,.2f}. "
                      f"Transaction cost, Ksh{fee:,.2f}. Amount you can transact within the day is {rem_limit:,.2f}. "
                      f"To reverse, forward this message to 456.")
            
            return True

>>>>>>> 90f26134e12423dae4455a9bd4164f27843b7d4c
        else:
            print(f"\033[91mInsufficient Funds. You need {total_to_deduct:,.2f} KES.\033[0m")
            return False

<<<<<<< HEAD
=======
    #Core Services with Tag mapping
>>>>>>> 90f26134e12423dae4455a9bd4164f27843b7d4c
    def send_money(self, user, phone, amt, pin, tag="Personal"): 
        return self._execute_transaction(user, phone, amt, "Send Money", pin, tag=tag)
    
    def buy_airtime(self, user, phone, amt, pin): 
        return self._execute_transaction(user, phone, amt, "Airtime", pin, tag="Utilities")
    
    def buy_goods(self, user, till, amt, pin, tag="Shopping"): 
        return self._execute_transaction(user, till, amt, "Buy Goods", pin, tag=tag)
    
    def pochi(self, user, phone, amt, pin, tag="Business"): 
        return self._execute_transaction(user, phone, amt, "Pochi", pin, tag=tag)
    
    def withdraw_cash(self, user, ag, st, amt, pin): 
        return self._execute_transaction(user, ag, amt, "Withdrawal", pin, {"agent": ag, "store": st}, tag="Cash")
    
    def paybill(self, user, bz, ac, amt, pin, tag="Bills"): 
        return self._execute_transaction(user, bz, amt, "Paybill", pin, {"biz": bz, "acc": ac}, tag=tag)

<<<<<<< HEAD
    def bank_service(self, user, bank, acc, amt, direction, b_pin, m_pin=None):
        db = self._load_db()
        bank_accounts = db.get("BANK_ACCOUNTS", {}).get(bank, {})
        bank_data = bank_accounts.get(acc)

        if not bank_data or str(bank_data['pin']) != str(b_pin):
            print("\033[91mBank Auth Failed: Incorrect Bank PIN.\033[0m"); return False
        
        if direction == "IN" and bank_data['balance'] < amt:
            print(f"\033[91m[!] Insufficient Bank Funds.\033[0m"); return False

        txn_type = "Bank_Topup" if direction == "IN" else "Bank_Transfer"
        tag = "Income" if direction == "IN" else "Savings"
        auth_pin = m_pin if m_pin else b_pin

        if self._execute_transaction(user, bank, amt, txn_type, auth_pin, {"acc": acc}, tag=tag):
=======
    #Financial Services
    def bank_service(self, user, bank, acc, amt, direction, b_pin, m_pin=None):
        db = self._load_db()
        bank_data = db.get("BANK_ACCOUNTS", {}).get(bank, {}).get(acc)
        if not bank_data or str(bank_data['pin']) != str(b_pin):
            print("\033[91mBank Auth Failed: Incorrect Bank PIN.\033[0m"); return False
        
        #Prevent Bank Overdraft when Top-up up M-Pesa
        if direction == "IN" and bank_data['balance'] < amt:
            print(f"\033[91m[!] Insufficient Bank Funds. Available: {bank_data['balance']:,.2f} KES\033[0m")
            return False

        txn_type = "Bank_Topup" if direction == "IN" else "Bank_Transfer"
        tag = "Income" if direction == "IN" else "Savings"
        
        if self._execute_transaction(user, bank, amt, txn_type, (m_pin if m_pin else b_pin), {"acc": acc}, tag=tag):
>>>>>>> 90f26134e12423dae4455a9bd4164f27843b7d4c
            if direction == "IN": bank_data['balance'] -= amt
            else: bank_data['balance'] += amt
            db["BANK_ACCOUNTS"][bank][acc] = bank_data
            self._save_db(db)
            return True
        return False
<<<<<<< HEAD
    def crypto_service(self, user, wallet_addr, kes_amount, direction, asset_name, coin_amount, wallet_pin, mpesa_pin):
        """
        Executes Crypto trades using Dual-PIN Authorization.
        """
        db = self._load_db()
        wallets = db.get("CRYPTO_WALLETS", {})
        wallet = wallets.get(wallet_addr)

        # Broker-Level Security: Verify the Account PIN
        if not wallet or str(wallet.get('pin')) != str(wallet_pin):
            print("\033[91m[!] Broker Auth Failed: Incorrect Account PIN.\033[0m")
            return False

        # Asset Check: Ensure enough crypto is available for liquidation
        if direction == "SELL" and wallet['balance'] < coin_amount:
            print(f"\033[91mInsufficient {asset_name} Units. Available: {wallet['balance']:.8f}\033[0m")
            return False

        # Transaction Preparation
        txn_type = "Crypto_Sell" if direction == "SELL" else "Crypto_Buy"
        
        # FIX: Use 'coin_amount' here because that is what is in your function arguments
        meta_data = {
            "wallet": wallet_addr, 
            "asset": asset_name, 
            "units": coin_amount, 
            "account_name": wallet.get('account name', 'Crypto Wallet')
        }

        # M-PESA Settlement
        if self._execute_transaction(user, wallet_addr, kes_amount, txn_type, mpesa_pin, meta_data, tag="Investment"):
            
            # Post-Trade Balance Update
            if direction == "SELL":
                wallet['balance'] -= coin_amount
            else:
                wallet['balance'] += coin_amount
            
            # Sync back to database
            db["CRYPTO_WALLETS"][wallet_addr] = wallet
            self._save_db(db)
            return True
            
=======

    #Crypto Service
    def crypto_service(self, user, wallet_addr, kes_amount, direction, asset_name, coin_amount, wallet_pin, mpesa_pin=None):
        db = self._load_db()
        wallet = db.get("CRYPTO_WALLETS", {}).get(wallet_addr)
        if not wallet or str(wallet['pin']) != str(wallet_pin):
            print("\033[91mCrypto Auth Failed: Incorrect Wallet PIN.\033[0m"); return False

        #Prevent selling more crypto than you own
        if direction == "SELL" and wallet['balance'] < coin_amount:
            print(f"\033[91m[!] Insufficient {asset_name} Units.")
            print(f"Available: {wallet['balance']:.6f} | Requested: {coin_amount:.6f}\033[0m")
            return False

        txn_type = "Crypto_Sell" if direction == "SELL" else "Crypto_Buy"
        tag = "Investment"
        meta_data = {"wallet": wallet_addr, "asset": asset_name, "units": coin_amount}

        if self._execute_transaction(user, wallet_addr, kes_amount, txn_type, (mpesa_pin if mpesa_pin else wallet_pin), meta_data, tag=tag):
            if direction == "SELL": wallet['balance'] -= coin_amount
            else: wallet['balance'] += coin_amount
            db["CRYPTO_WALLETS"][wallet_addr] = wallet
            self._save_db(db)
            return True
>>>>>>> 90f26134e12423dae4455a9bd4164f27843b7d4c
        return False