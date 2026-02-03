import pandas as pd
import ast
from datetime import datetime

class Dashboard:
    @staticmethod
    def _load_data(filename):
        try:
            df = pd.read_csv(filename)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            return df
        except (FileNotFoundError, pd.errors.EmptyDataError):
            return None

    @staticmethod
    def show_filtered_data(filename, category_name):
        """Filtered Transactions with Direction, Tags, and Balance After"""
        df = Dashboard._load_data(filename)
        if df is None or df.empty:
<<<<<<< HEAD
            print("\n\033[91mNo transaction history found.\033[0m")
=======
            print("\n\033[91m[!] No transaction history found.\033[0m")
>>>>>>> 90f26134e12423dae4455a9bd4164f27843b7d4c
            return

        print(f"\n{category_name.upper()} HISTORY")
        #Ensure comparison works even with different case types
        filtered = df[df['type'].str.replace('_', ' ').str.contains(category_name, case=False, na=False)]
        
        if filtered.empty:
            print(f"No transactions found for: {category_name}.")
        else:
            filtered = filtered.sort_values(by='timestamp', ascending=False)
<<<<<<< HEAD
            print(f"{'TIMESTAMP':<20} | {'TRANSACTION TYPE':<8} | {'TAG':<10} | {'RECIPIENT':<15} | {'AMOUNT':>10} | {'BALANCE AFTER':>12} | {'BALANCE BEFORE':>12}")
=======
            print(f"{'TIMESTAMP':<20} | {'TRANSACTION TYPE':<8} | {'TAG':<12} | {'RECIPIENT':<20} | {'AMOUNT':>10} | {'BAL AFTER':>12}")
>>>>>>> 90f26134e12423dae4455a9bd4164f27843b7d4c
            print("-" * 105)
            
            incoming_types = ["Bank_Topup", "Crypto_Sell"]
            for _, row in filtered.iterrows():
                is_income = row['type'] in incoming_types
                direction = "RECEIVED" if is_income else "SENT"
                color = "\033[92m" if is_income else "\033[91m"
                
                print(f"{str(row['timestamp'])[:19]:<20} | {color}{direction:<8}\033[0m | {str(row['tag']):<12} | "
<<<<<<< HEAD
                      f"{str(row['recipient'])[:20]:<20} | {color}{row['amount']:>10,.2f}\033[0m | {row['balance_after']:>12,.2f} | {row['balance_before']:>12,.2f}")
=======
                      f"{str(row['recipient'])[:20]:<20} | {color}{row['amount']:>10,.2f}\033[0m | {row['balance_after']:>12,.2f}")
>>>>>>> 90f26134e12423dae4455a9bd4164f27843b7d4c

    @staticmethod
    def show_full_statement(filename):
        """Complete Ledger Statement with Balance Tracking"""
        df = Dashboard._load_data(filename)
        if df is None or df.empty:
<<<<<<< HEAD
            print("\n\033[91mNo transaction history found.\033[0m")
=======
            print("\n\033[91m[!] No transaction history found.\033[0m")
>>>>>>> 90f26134e12423dae4455a9bd4164f27843b7d4c
            return
        
        recent_df = df.sort_values(by='timestamp', ascending=False)
        
        print("\n" + "="*155)
<<<<<<< HEAD
        print(f"{'TIMESTAMP':<20} | {'TYPE':<12} | {'TAG':<10} | {'RECIPIENT/ASSET':<25} | {'AMOUNT':>12} | {'FEE':>8} | {'BALANCE BEFORE':>15} | {'BALANCE AFTER':>15}")
=======
        print(f"{'TIMESTAMP':<20} | {'TYPE':<12} | {'TAG':<10} | {'RECIPIENT/ASSET':<25} | {'AMOUNT':>12} | {'FEE':>8} | {'BAL BEFORE':>15} | {'BAL AFTER':>15}")
>>>>>>> 90f26134e12423dae4455a9bd4164f27843b7d4c
        print("-" * 155)
        
        incoming_types = ["Bank_Topup", "Crypto_Sell"]
        
        for _, row in recent_df.iterrows():
            is_income = row['type'] in incoming_types
            color_code = "\033[92m" if is_income else "\033[91m"
            reset = "\033[0m"
            
            detail_display = str(row['recipient'])[:25]
            if pd.notna(row['metadata']) and row['metadata'] != 'None':
                try:
                    meta_dict = ast.literal_eval(row['metadata'])
                    if isinstance(meta_dict, dict):
                        if 'asset' in meta_dict:
                            detail_display = f"[{meta_dict['asset']}] {detail_display}"
                        elif 'acc' in meta_dict:
                            detail_display = f"Acc: {meta_dict['acc']}"
                except:
                    pass

            print(f"{str(row['timestamp'])[:19]:<20} | "
                  f"{row['type']:<12} | "
                  f"{str(row['tag']):<10} | "
                  f"{detail_display:<25} | "
                  f"{color_code}{row['amount']:>12,.2f}{reset} | "
                  f"{row['fee']:>8.2f} | "
                  f"{row['balance_before']:>15,.2f} | "
                  f"{color_code}{row['balance_after']:>15,.2f}{reset}")
        
        print("="*155)
        current_bal = df.sort_values(by='timestamp').iloc[-1]['balance_after']
        print(f"Final Account Balance: {current_bal:,.2f} KES")
<<<<<<< HEAD
        print("="*155)
=======
        print("="*155)

    @staticmethod
    def show_forecasting_analytics(filename):
        """NEW: Grouped spending by Tag to aid forecasting models"""
        df = Dashboard._load_data(filename)
        if df is None or df.empty: return

        #Filter only outgoing transactions for spending analysis
        incoming_types = ["Bank_Topup", "Crypto_Sell"]
        spending_df = df[~df['type'].isin(incoming_types)]

        print("\n--- SPENDING ANALYTICS (By Tag) ---")
        if not spending_df.empty:
            summary = spending_df.groupby('tag')['amount'].sum().sort_values(ascending=False)
            total_spent = summary.sum()
            
            print(f"{'CATEGORY (TAG)':<15} | {'TOTAL SPENT':>15} | {'% OF TOTAL'}")
            print("-" * 50)
            for tag, amt in summary.items():
                percentage = (amt / total_spent) * 100
                print(f"{tag:<15} | {amt:>15,.2f} | {percentage:>10.1f}%")
            print("-" * 50)
            print(f"{'TOTAL':<15} | {total_spent:>15,.2f} | 100.0%")
        else:
            print("No spending data recorded yet.")
    @staticmethod
    def show_monthly_report(filename):
        df = Dashboard._load_data(filename)
        if df is None or df.empty: return

        #Get the current Month and Year dynamically
        report_title = datetime.now().strftime("%B %Y").upper() + " FINANCIAL REPORT"

        #Financial Overview
        start_bal = df.sort_values('timestamp').iloc[0]['balance_before']
        end_bal = df.sort_values('timestamp').iloc[-1]['balance_after']
        
        incoming_types = ["Bank_Topup", "Crypto_Sell"]
        total_in = df[df['type'].isin(incoming_types)]['amount'].sum()
        total_out = df[~df['type'].isin(incoming_types)]['amount'].sum()

        print("\n" + "╔" + "═"*50 + "╗")
        print(f"║ {report_title:^48} ║")
        print("╠" + "═"*50 + "╣")
        print(f"║ Opening Balance: {start_bal:>31,.2f} ║")
        print(f"║ Total Money In:  \033[92m{total_in:>31,.2f}\033[0m ║")
        print(f"║ Total Money Out: \033[91m{total_out:>31,.2f}\033[0m ║")
        print(f"║ Closing Balance: {end_bal:>31,.2f} ║")
        print("╚" + "═"*50 + "╝")

        Dashboard.show_forecasting_analytics(filename)
>>>>>>> 90f26134e12423dae4455a9bd4164f27843b7d4c
