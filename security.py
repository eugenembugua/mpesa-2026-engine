import json
import time
from datetime import datetime, timedelta

class SecuritySystem:
    def __init__(self, registered_phone, password, pin, secret_path='secret.json'):
        self.__phone = registered_phone
        self.__password = password
        self.__pin = pin
        self.secret_path = secret_path
        self.max_attempts = 3
<<<<<<< HEAD
        self.lockout_duration = 5 # minutes
=======
        self.lockout_duration = 10
>>>>>>> 90f26134e12423dae4455a9bd4164f27843b7d4c

    #Secret File Handlers
    def load_secrets(self):
        try:
            with open(self.secret_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_secrets(self, data):
        try:
            with open(self.secret_path, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Critical Sync Error: {e}")

<<<<<<< HEAD
    #Login Logic (Dual Step)
    def verify_login_step_1(self, input_phone):
        """Validates phone number before password entry."""
        data = self.load_secrets()
        
        if self.is_locked(data):
            return False

        if str(input_phone) == str(self.__phone):
            return True
        else:
            self.handle_failed_attempt(data)
            return False

    def authenticate_app_step_2(self, input_password):
        """Validates password after phone is confirmed."""
        data = self.load_secrets()
        
        if input_password == self.__password:
            self.reset_attempts(data)
            current_time = datetime.now().strftime("%H:%M:%S")
            print(f"\nLogin Successful at {current_time}.")
            return True
        else:
            self.handle_failed_attempt(data)
            return False

    #PIN Management (Transaction Level)
=======
    #Authentication & PIN Management
    def authenticate_app(self, input_phone, input_password):
        if input_phone == self.__phone and input_password == self.__password:
            current_time = datetime.now().strftime("%H:%M:%S")
            print(f"\n\033[92m[SECURITY]\033[0m Login Successful at {current_time}.")
            return True
        return False

>>>>>>> 90f26134e12423dae4455a9bd4164f27843b7d4c
    def verify_pin(self, input_pin):
        data = self.load_secrets()
        
        if self.is_locked(data):
            return False

        if str(input_pin) == str(self.__pin):
            self.reset_attempts(data)
            return True
        else:
            self.handle_failed_attempt(data)
            return False

    def update_pin(self, new_pin):
<<<<<<< HEAD
=======
        """Allows user to change their PIN (Option 6 -> 3)"""
>>>>>>> 90f26134e12423dae4455a9bd4164f27843b7d4c
        self.__pin = str(new_pin)
        return True

    #Lockout Logic
    def is_locked(self, data):
        lockout_time_str = data.get("lockout_until")
        if lockout_time_str:
            lockout_until = datetime.fromisoformat(lockout_time_str)
<<<<<<< HEAD
            
            # Check if current time is still before the lockout expiration
            if datetime.now() < lockout_until:
                print(f"\n\033[91mSECURITY LOCKOUT ACTIVE\033[0m")
                
                #Live Countdown Loop
                while datetime.now() < lockout_until:
                    remaining = lockout_until - datetime.now()
                    mins, secs = divmod(int(remaining.total_seconds()), 60)
                    # \r allows the line to overwrite itself for the ticking effect
                    print(f"\rTime remaining: {mins:02d}:{secs:02d} ", end="", flush=True)
                    time.sleep(1)
                
                print("\n\n\033[92mLockout lifted. You may try again.\033[0m")
                self.reset_attempts(data)
                return False #Let them through now that time is up
        return False
    
=======
            if datetime.now() < lockout_until:
                remaining = (lockout_until - datetime.now()).total_seconds() // 60
                print(f"\033[91m[LOCKED] Too many failed attempts. Try again in {int(remaining)} mins.\033[0m")
                return True
        return False

>>>>>>> 90f26134e12423dae4455a9bd4164f27843b7d4c
    def handle_failed_attempt(self, data):
        attempts = data.get("failed_attempts", 0) + 1
        data["failed_attempts"] = attempts
        
        if attempts >= self.max_attempts:
            lock_time = datetime.now() + timedelta(minutes=self.lockout_duration)
            data["lockout_until"] = lock_time.isoformat()
<<<<<<< HEAD
            print(f"\n\033[91mAccount locked for {self.lockout_duration} mins after {attempts} failures.\033[0m")
        else:
            print(f"\033[93mInvalid Credential. {self.max_attempts - attempts} attempt(s) remaining.\033[0m")
        
=======
            print(f"\033[91m[SECURITY] 3 failures detected. Account locked for {self.lockout_duration} mins.\033[0m")
        else:
            print(f"\033[93m[!] Invalid PIN. {self.max_attempts - attempts} attempts remaining.\033[0m")
>>>>>>> 90f26134e12423dae4455a9bd4164f27843b7d4c
        self.save_secrets(data)

    def reset_attempts(self, data):
        data["failed_attempts"] = 0
        data["lockout_until"] = None
        self.save_secrets(data)

    #Daily Limit Logic
    def check_and_reset_limit(self, data):
        today = datetime.now().strftime('%Y-%m-%d')
        if data.get("last_reset_date") != today:
            data["spent_today"] = 0.0
            data["last_reset_date"] = today
            self.save_secrets(data) 
            return True
        return False

    def is_within_limit(self, amount, data):
        return (float(data.get("spent_today", 0)) + amount) <= float(data.get("daily_limit", 500000))