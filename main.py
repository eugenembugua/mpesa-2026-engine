<<<<<<< HEAD
import stdiomask, hashlib
import os, sys
=======
import stdiomask
>>>>>>> 90f26134e12423dae4455a9bd4164f27843b7d4c
import json, getpass, datetime, time
from datetime import datetime
from models import User
from engine import MPesaEngine
from security import SecuritySystem
from data_logger import DataLogger
from dashboard import Dashboard

def show_logo():
    logo = """
<<<<<<< HEAD
    \033[92mMMMMMMMM               \033[91mPPPPPPPPPP   EEEEEEEEE   SSSSSSSSS      A     
    \033[92mM  MM  M               \033[91mP        P   E           S             AAA    
=======
    \033[92mMMMMMMMM               \033[91mPPPPPPPPPP   EEEEEEEEE   SSSSSSSSS       A     
    \033[92mM  MM  M               \033[91mP        P   E           S             A A    
>>>>>>> 90f26134e12423dae4455a9bd4164f27843b7d4c
    \033[92mM  MM  M  \033[37m----------   \033[91mPPPPPPPPPP   EEEEEEEEE   SSSSSSSSS    AAAAA   
    \033[92mM      M               \033[91mP            E                   S   A     A  
    \033[92mM      M               \033[91mP            EEEEEEEEE   SSSSSSSSS  A       A 
    \033[0m"""
    print(logo)
    print("      \033[1mSimple. Transparent and Honest.\033[0m")
    print("==========================================")

def load_secrets(filepath='secret.json'):
    try:
        with open(filepath, 'r') as f: return json.load(f)
    except FileNotFoundError:
        print(f"Error: {filepath} not found.")
        return None

def save_secrets(data, filepath='secret.json'):
    try:
        with open(filepath, 'w') as f: json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Sync error: {e}")

def get_tag():
<<<<<<< HEAD
    """Categorizes transactions to provide data for forecasting"""
=======
    """Helper to categorize transactions for forecasting"""
>>>>>>> 90f26134e12423dae4455a9bd4164f27843b7d4c
    tags = {
        "1": "Food", "2": "Clothes", "3": "Transport", 
        "4": "Rent/Bills", "5": "Leisure", "6": "Business", 
        "7": "Family", "8": "Savings", "9": "Debt"
    }
    print("\nCategorize this expense:")
    for k, v in tags.items(): print(f"{k}. {v}")
    choice = input("Select Tag (Press Enter for 'General'): ")
    return tags.get(choice, "General")

def main():
    show_logo()
    data = load_secrets()
    if not data: return

<<<<<<< HEAD
    #Year 2026 Data File
    data_file = "mpesa_data_2026.csv"
    TIMEOUT_SECONDS = 120 
    
=======
    data_file = "mpesa_data_2026.csv"
    TIMEOUT_SECONDS = 120 #2 Minutes
    
    #Initialize Core Systems
>>>>>>> 90f26134e12423dae4455a9bd4164f27843b7d4c
    sec = SecuritySystem(data["registered_phone"], data["app_password"], data["transaction_pin"])
    logger = DataLogger()
    mpesa = MPesaEngine(logger, sec)
    user = User(data["user_name"], data["registered_phone"], data["balance"])

    print("==========================================")
<<<<<<< HEAD
    print(f"             M-PESA MOBILE APP              ")
    print(f"      {datetime.now().strftime('%A, %d %B %Y')}")
    print("==========================================")
    
    while True: #Global App Loop
        authenticated = False
        
        #LOGIN PHASE
        while not authenticated:
            current_data = load_secrets()
            sec.is_locked(current_data) 

            print("\n\033[1m   SECURE LOGIN\033[0m")
            in_phone = stdiomask.getpass("Enter Phone Number: ", mask='•')
            if not sec.verify_login_step_1(in_phone):
                continue 

            in_pass = stdiomask.getpass("Enter App Password: ", mask='*')
            if sec.authenticate_app_step_2(in_pass):
                authenticated = True
                last_activity_time = time.time()
            else:
                continue 

        #MENU PHASE
        while authenticated:
            if time.time() - last_activity_time > TIMEOUT_SECONDS:
                print("\n\033[91m\033[1mSession Expired. Please log in again.\033[0m")
                authenticated = False 
                break

            print(f"\n{user.get_full_name()} | Balance: {user.account.get_balance():,.2f} KES")
            print("Mpesa Menu Options:")
            print("1. Send Money\n2. Withdraw Cash\n3. Buy Airtime\n4. Lipa na M-Pesa\n5. Financial Services\n6. My Account\n0. Logout")
            
            choice = input("Select Option: ")
            if choice: last_activity_time = time.time()
            
            transaction_success = False

            if choice == "0":
                print(f"Logging out {data['user_name']}...")
                authenticated = False
                break

            #SEND MONEY
            elif choice == "1":
                print("1. Send to Favorites\n2. Enter Phone Number\n3. Back")
                send_choice = input("Select: ")
                ph = None 
                if send_choice == "1":
                    favs = {"1": ("Mom", "0712345678"), "2": ("Babe", "0718654567"), "3": ("Landlord", "0722000111")}
                    for k, v in favs.items(): print(f"{k}. {v[0]} ({v[1]})")
                    f_sel = input("Select (0 to back): ")
                    if f_sel in favs: ph = favs[f_sel][1]
                elif send_choice == "2":
                    ph = input("Enter Phone: ")
                
                if ph:
                    amt = int(input("Amount: "))
                    tag = get_tag()
                    mpesa.show_preview(amt, "Send Money", ph)
                    if input("Confirm? (y/n): ").lower() == 'y':
                        pin = stdiomask.getpass("M-PESA PIN: ", mask='•')
                        transaction_success = mpesa.send_money(user, ph, amt, pin, tag=tag)

            #WITHDRAWAL
            elif choice == "2": 
                ag = input("Agent No: "); st = input("Store No: "); amt = int(input("Amount: "))
                mpesa.show_preview(amt, "Withdrawal", ag, store_id=st)
                if input("Confirm? (y/n): ").lower() == "y":
                    pin = stdiomask.getpass("M-PESA PIN: ", mask='•')
                    transaction_success = mpesa.withdraw_cash(user, ag, st, amt, pin)

            #BUY AIRTIME
            elif choice == "3": 
                print("1. My Phone\n2. Other Phone\n0. Back")
                air_opt = input("Select: ")
                ph = data["registered_phone"] if air_opt == "1" else input("Phone: ") if air_opt == "2" else None
                if ph:
                    amt = int(input("Amount: "))
                    mpesa.show_preview(amt, "Airtime", ph)
                    if input("Confirm? (y/n): ").lower() == 'y':
                        pin = stdiomask.getpass("M-PESA PIN: ", mask='•')
                        transaction_success = mpesa.buy_airtime(user, ph, amt, pin)

            #LIPA NA M-PESA
            elif choice == "4": 
                print("\n1. Paybill\n2. Buy Goods\n3. Pochi\n0. Back")
                lp = input("Select Option: ")
                if lp in ["1", "2", "3"]:
                    tag = get_tag()
                    if lp == "1":
                        bz = input("Paybill: "); ac = input("Account no: "); amt = int(input("Amount: "))
                        mpesa.show_preview(amt, "Paybill", bz, acc_no=ac)
                        if input("Confirm? (y/n): ").lower() == "y":
                            pin = stdiomask.getpass("PIN: ", mask='•')
                            transaction_success = mpesa.paybill(user, bz, ac, amt, pin, tag=tag)
                    elif lp == "2":
                        tl = input("Till no: "); amt = int(input("Amount: "))
                        mpesa.show_preview(amt, "Buy Goods & Services", tl)
                        if input("Confirm? (y/n): ").lower() == "y":
                            pin = stdiomask.getpass("PIN: ", mask='•')
                            transaction_success = mpesa.buy_goods(user, tl, amt, pin, tag=tag)
                    elif lp == "3":
                        ph = input("Seller Phone no: "); amt = int(input("Amount: "))
                        mpesa.show_preview(amt, "Pochi", ph)
                        if input("Confirm? (y/n): ").lower() == "y":
                            pin = stdiomask.getpass("PIN: ", mask='•')
                            transaction_success = mpesa.pochi(user, ph, amt, pin, tag=tag)

            #FINANCIAL SERVICES
            elif choice == "5": 
                print("\n1. Bank\n2. Crypto\n0. Back")
                sub = input("Select: ")
                if sub == "1":
                    db = mpesa._load_db()
                    banks = list(db.get("BANK_ACCOUNTS", {}).keys())
                    for i, b in enumerate(banks, 1): print(f"{i}. {b}")
                    bnk_name = banks[int(input("Bank Index: ")) - 1]
                    rel_accs = db["BANK_ACCOUNTS"][bnk_name]
                    acc_list = list(rel_accs.keys())
                    for i, a in enumerate(acc_list, 1): print(f"{i}. {a} ({rel_accs[a]['name']})")
                    acc = acc_list[int(input("Account no: ")) - 1]
                    mode = "IN" if input("1. Deposit (Bank to Mpesa)\n2. Withdraw (Mpesa to Bank)\nSelect: ") == "1" else "OUT"
                    amt = int(input("Amount: "))
                    bp = stdiomask.getpass(f"Enter {bnk_name} PIN: ", mask='•')
                    mp = stdiomask.getpass("Enter M-PESA PIN: ", mask='•')
                    transaction_success = mpesa.bank_service(user, bnk_name, acc, amt, mode, bp, mp)
                    
                elif sub == "2":
                    db = mpesa._load_db()
                    wallets = db.get("CRYPTO_WALLETS", {})
                    
                    #Select Broker Company
                    unique_brokers = list(set([w['name'] for w in wallets.values()]))
                    print("\nSELECT CRYPTO BROKER")
                    for i, b_name in enumerate(unique_brokers, 1): 
                        print(f"{i}. {b_name}")
                    
                    broker_choice = input("Select Broker (or Enter to cancel): ")
                    if not broker_choice.isdigit() or int(broker_choice) > len(unique_brokers):
                        print("\033[91mInvalid selection.\033[0m")
                        continue
                    selected_broker = unique_brokers[int(broker_choice) - 1]

                    #Select Crypto Asset
                    print(f"\nAVAILABLE ASSETS FOR {selected_broker}")
                    assets = list(set([w['asset'] for w in wallets.values() if w['name'] == selected_broker]))
                    for i, asset_name in enumerate(assets, 1):
                        print(f"{i}. {asset_name}")
                    
                    asset_choice = input("Select Asset: ")
                    if not asset_choice.isdigit() or int(asset_choice) > len(assets):
                        print("\033[91mInvalid asset selection.\033[0m")
                        continue
                    selected_asset = assets[int(asset_choice) - 1]

                    #Enter Account No & Validate if asset exists in that account
                    input_addr = stdiomask.getpass("Enter Account No: ", mask="•")
                    wallet_data = wallets.get(input_addr)

                    if not wallet_data or wallet_data.get('name') != selected_broker or wallet_data.get('asset') != selected_asset:
                        print(f"\033[91mError: Asset {selected_asset} is not listed in this account or Broker mismatch.\033[0m")
                        continue

                    #Password Authentication
                    acc_pass = stdiomask.getpass("Enter Account Password: ", mask='•')
                    if wallet_data.get('password') != acc_pass:
                        print("\033[91mAlert: Wrong Account Password!\033[0m")
                        continue
                    
                    #Transaction Details
                    print("\nTRANSACTION DETAILS")
                    mode_input = input("1. Sell\n2. Buy\nSelect Action: ")
                    mode = "selling" if mode_input == "1" else "buying" if mode_input == "2" else None
                    
                    if not mode:
                        print("\033[91mInvalid action.\033[0m")
                        continue

                    amt_input = input(f"Enter KES Amount: ")
                    if not amt_input.isdigit():
                        print("\033[91mInvalid amount.\033[0m")
                        continue
                        
                    kes_total = int(amt_input)
                    #Calculation for cost and tax
                    transaction_cost = kes_total * 0.01 
                    tax = transaction_cost * 0.16
                    
                    #Authentication Prompt
                    print(f"\n\033[94mDo you authenticate the {mode} of {selected_asset} worth {kes_total:,} KES?")
                    print(f"Applicable transaction cost: {transaction_cost:.2f} KES and Tax: {tax:.2f} KES\033[0m")
                    
                    print("1. Yes")
                    print("2. No")
                    confirm = input("Select Option: ")
                    
                    if confirm == "1":
                        #Dual PIN Entry
                        acc_pin = stdiomask.getpass(f"Enter {selected_broker} Account PIN: ", mask='•')
                        mpesa_pin = stdiomask.getpass("Enter M-PESA PIN: ", mask='•')
                        
                        #Verify Account PIN from JSON
                        if acc_pin == wallet_data.get('pin'):
                            #Call the service
                            rate = db.get("CRYPTO_RATES", {}).get(selected_asset, 1)
                            coin_units = kes_total / rate
                            mpesa.crypto_service(user, input_addr, kes_total, mode.upper(), selected_asset, coin_units, acc_pin, mpesa_pin)
                        else:
                            print("\033[91mIncorrect Account PIN. Transaction cancelled.\033[0m")
                    else:
                        print("Returning to main menu...")
                        continue

            #MY ACCOUNT
            elif choice == "6":
                print("\n1. Full Statement")
                print("2. Category Statements")
                print("3. Change PIN")
                print("0. Back")
                ac_choice = input("Select Option: ")

                if ac_choice == "1":
                    target_email = input("Enter Email Address: ")
                    pin_input = stdiomask.getpass("Enter M-PESA PIN: ", mask='•')
                    if sec.verify_pin(pin_input):
                        from statement_service import send_yearly_statement
                        send_yearly_statement(target_email, data_file)

                elif ac_choice == "2":
                    print("\nSELECT CATEGORY FOR STATEMENT")
                    print("1. Send Money")
                    print("2. Airtime Purchases")
                    print("3. Paybill Payments")
                    print("4. Buy Goods (Till) Payments")
                    print("5. Pochi la Biashara Payments")
                    print("0. Back")
                    
                    cat_choice = input("Select Category: ")
                    
                    #Mapping user selection to the 'type' column strings to match CSV
                    category_map = {
                        "1": "Send Money",
                        "2": "Airtime",
                        "3": "Paybill",
                        "4": "Buy Goods",
                        "5": "Pochi"
                    }

                    if cat_choice in category_map:
                        # Dashboard.show_filtered_data(filename, category_name)
                        Dashboard.show_filtered_data(data_file, category_map[cat_choice])
                    elif cat_choice == "0":
                        continue

                elif ac_choice == "3":
                    if sec.verify_pin(stdiomask.getpass("Current PIN: ", mask='•')):
                        np = stdiomask.getpass("New PIN: ", mask='•')
                        if np == stdiomask.getpass("Confirm: ", mask='•'):
                            sec.update_pin(np)
                            data["transaction_pin"] = np
                            save_secrets(data)
                            print("\033[92mPIN Updated Successfully.\033[0m")
            #LOGOUT & EXIT
            elif choice == "0":
                print(f"\n\033[93mLogging out {data['user_name']}...\033[0m")
                time.sleep(1) #Allows the user to see the logout message
                
                #Wipes the terminal history for security
                os.system('cls' if os.name == 'nt' else 'clear')
                
                print("\033[1mSession terminated.\033[0m")
                sys.exit() #Completely closes the app
                
            #POST-TRANSACTION SYNC
            if transaction_success:
                data["balance"] = user.account.get_balance()
                save_secrets(data)

=======
    print(f"            M-PESA MOBILE APP              ")
    print(f"      {datetime.now().strftime('%A, %d %B %Y')}")
    print("==========================================")
    
    print("\033[1m   SECURE LOGIN\033[0m")
    in_phone = stdiomask.getpass("Enter Phone Number: ", mask='•')
    in_pass = stdiomask.getpass("Enter App Password: ", mask='*')

    if not sec.authenticate_app(in_phone, in_pass):
        return
    
    #Start activity timer after successful login
    last_activity_time = time.time()

    while True:
        #Check for Session Timeout
        if time.time() - last_activity_time > TIMEOUT_SECONDS:
            print("\n\033[91m[!] Session Expired. Please log in again.\033[0m")
            break

        print(f"\n{user.get_full_name()} | Balance: {user.account.get_balance():,.2f} KES")
        print("Mpesa Menu Options:")
        print("1. Send Money\n2. Withdraw Cash\n3. Buy Airtime\n4. Lipa na M-Pesa\n5. Financial Services\n6. My Account\n0. Logout")
        
        choice = input("Select Option: ")
        if choice: last_activity_time = time.time() # Reset timer on input
        
        transaction_success = False 

        #SEND MONEY
        if choice == "1":
            print("1. Send to Favorites\n2. Enter Phone Number\n3. Back")
            send_choice = input("Select: ")
            ph = None 
            if send_choice == "1":
                favs = {"1": ("Mom", "0712345678"), "2": ("Babe", "0718654567"), "3": ("Landlord", "0722000111")}
                for k, v in favs.items(): print(f"{k}. {v[0]} ({v[1]})")
                f_sel = input("Select (0 to back): ")
                if f_sel in favs: ph = favs[f_sel][1]
            elif send_choice == "2":
                ph = input("Enter Phone: ")
            
            if ph:
                amt = int(input("Amount: "))
                tag = get_tag()
                mpesa.show_preview(amt, "Send Money", ph)
                if input("Confirm? (y/n): ").lower() == 'y':
                    pin = stdiomask.getpass("M-PESA PIN: ", mask='•')
                    transaction_success = mpesa.send_money(user, ph, amt, pin, tag=tag)

        #WITHDRAWAL
        elif choice == "2": 
            ag = input("Agent No: "); st = input("Store No: "); amt = int(input("Amount: "))
            mpesa.show_preview(amt, "Withdrawal", ag, store_id=st)
            if input("Confirm? (y/n): ").lower() == "y":
                pin = stdiomask.getpass("M-PESA PIN: ", mask='•')
                transaction_success = mpesa.withdraw_cash(user, ag, st, amt, pin)

        #BUY AIRTIME
        elif choice == "3": 
            print("1. My Phone\n2. Other Phone\n0. Back")
            air_opt = input("Select: ")
            ph = data["registered_phone"] if air_opt == "1" else input("Phone: ") if air_opt == "2" else None
            if ph:
                amt = int(input("Amount: "))
                mpesa.show_preview(amt, "Airtime", ph)
                if input("Confirm? (y/n): ").lower() == 'y':
                    pin = stdiomask.getpass("M-PESA PIN: ", mask='•')
                    transaction_success = mpesa.buy_airtime(user, ph, amt, pin)

        #LIPA NA M-PESA
        elif choice == "4": 
            print("\n1. Paybill\n2. Buy Goods\n3. Pochi\n0. Back")
            lp = input("Select: ")
            if lp in ["1", "2", "3"]:
                tag = get_tag()
                if lp == "1":
                    bz = input("Paybill: "); ac = input("Account: "); amt = int(input("Amount: "))
                    mpesa.show_preview(amt, "Paybill", bz, acc_no=ac)
                    if input("Confirm? (y/n): ").lower() == "y":
                        pin = stdiomask.getpass("PIN: ", mask='•')
                        transaction_success = mpesa.paybill(user, bz, ac, amt, pin, tag=tag)
                elif lp == "2":
                    tl = input("Till: "); amt = int(input("Amount: "))
                    mpesa.show_preview(amt, "Buy Goods", tl)
                    if input("Confirm? (y/n): ").lower() == "y":
                        pin = stdiomask.getpass("PIN: ", mask='•')
                        transaction_success = mpesa.buy_goods(user, tl, amt, pin, tag=tag)
                elif lp == "3":
                    ph = input("Phone: "); amt = int(input("Amount: "))
                    mpesa.show_preview(amt, "Pochi", ph)
                    if input("Confirm? (y/n): ").lower() == "y":
                        pin = stdiomask.getpass("PIN: ", mask='•')
                        transaction_success = mpesa.pochi(user, ph, amt, pin, tag=tag)

        #FINANCIAL SERVICES
        elif choice == "5": 
            print("\n1. Bank\n2. Crypto\n0. Back")
            sub = input("Select: ")
            if sub == "1":
                db = mpesa._load_db()
                banks = {"1": "KCB", "2": "EQUITY", "3": "CO-OP", "4": "ABSA", "5": "NCBA"}
                for k, v in banks.items(): print(f"{k}. {v}")
                bnk_name = banks.get(input("Bank: "), "OTHER")
                rel_accs = db.get("BANK_ACCOUNTS", {}).get(bnk_name, {})
                if not rel_accs: continue
                acc_list = list(rel_accs.keys())
                for i, a in enumerate(acc_list, 1): print(f"{i}. {a}")
                acc = acc_list[int(input("Account Index: ")) - 1]
                mode = "IN" if input("1. Deposit\n2. Withdraw\nSelect: ") == "1" else "OUT"
                amt = int(input("Amount: "))
                bp = stdiomask.getpass(f"{bnk_name} PIN: ", mask='•')
                mp = stdiomask.getpass("M-PESA PIN: ", mask='•')
                transaction_success = mpesa.bank_service(user, bnk_name, acc, amt, mode, bp, mp)
                
            elif sub == "2":
                db = mpesa._load_db()
                wallets = db.get("CRYPTO_WALLETS", {})
                w_list = list(wallets.keys())
                for i, addr in enumerate(w_list, 1): print(f"{i}. {wallets[addr]['name']} ({wallets[addr]['asset']})")
                addr = w_list[int(input("Select Wallet: ")) - 1]
                asset = wallets[addr]['asset']
                rate = db.get("CRYPTO_RATES", {}).get(asset, 0)
                mode = "SELL" if input("1. Sell\n2. Buy\nSelect: ") == "1" else "BUY"
                kes_total = int(input(f"Amount in KES to {mode.lower()}: "))
                coin_units = kes_total / rate
                print(f"\033[94m**Crypto Review:**\033[0m {mode} {coin_units:.6f} {asset} for {kes_total:,.2f} KES")
                wp = stdiomask.getpass("Wallet PIN: ", mask='•')
                mp = stdiomask.getpass("M-PESA PIN: ", mask='•')
                transaction_success = mpesa.crypto_service(user, addr, kes_total, mode, asset, coin_units, wp, mp)

        #MY ACCOUNT
        elif choice == "6":
            print("\n1. Filtered\n2. Full\n3. Monthly Report\n4. Change PIN\n0. Back")
            ac_choice = input("Select: ")
            if ac_choice == "2": Dashboard.show_full_statement(data_file)
            elif ac_choice == "3": Dashboard.show_monthly_report(data_file)
            elif ac_choice == "4":
                if sec.verify_pin(stdiomask.getpass("Current PIN: ", mask='•')):
                    np = stdiomask.getpass("New PIN: ", mask='•')
                    if np == stdiomask.getpass("Confirm: ", mask='•'):
                        sec.update_pin(np); data["transaction_pin"] = np; save_secrets(data)
                        print("\033[92mSuccess.\033[0m")

        elif choice == "0":
            print(f"Goodbye {data['user_name']}!"); break

        if transaction_success:
            data["balance"] = user.account.get_balance()
            save_secrets(data)

    #Logout Cleanup
    del in_phone, in_pass
>>>>>>> 90f26134e12423dae4455a9bd4164f27843b7d4c
    print("\033[1mSession Closed.\033[0m")

if __name__ == "__main__":
    main()