import csv
import uuid
import os
<<<<<<< HEAD
import hashlib
=======
>>>>>>> 90f26134e12423dae4455a9bd4164f27843b7d4c
from datetime import datetime

class DataLogger:
    def __init__(self, filename="mpesa_data_2026.csv"):
        self.filename = filename
<<<<<<< HEAD
        self.audit_file = "file_integrity.hash" #Store the "Seal"
=======
>>>>>>> 90f26134e12423dae4455a9bd4164f27843b7d4c
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    "txn_id", "timestamp", "sender", "recipient", 
                    "type", "amount", "fee", "balance_before", 
                    "balance_after", "tag", "metadata"
                ])

    def log_transaction(self, s, r, t, a, f, b_before, b_after, tag="General", meta=None, timestamp=None):
        """
        s: sender, r: recipient, t: type, a: amount, f: fee, 
        b_before: Balance Before, b_after: Balance After, tag: Spending Category
        """
        if timestamp is None:
            timestamp = datetime.now()
            
        txn_id = f"U{str(uuid.uuid4())[:8].upper()}" 
        
        with open(self.filename, 'a', newline='') as file:
            csv.writer(file).writerow([
                txn_id, 
                timestamp.strftime("%Y-%m-%d %H:%M:%S"), 
                s, r, t, a, f, b_before, b_after, tag, meta
            ])
<<<<<<< HEAD
        self._seal_file()
        return txn_id
    
    def _seal_file(self):
        """Generates a SHA-256 hash to detect if the CSV was altered."""
        with open(self.filename, "rb") as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
        with open(self.audit_file, "w") as f:
            f.write(file_hash)
        #Set file to Read-Only(Linux)
        os.chmod(self.filename, 0o444) 

    def verify_integrity(self):
        """Checks if the CSV has been tampered with."""
        if not os.path.exists(self.audit_file): return False
        with open(self.filename, "rb") as f:
            current_hash = hashlib.sha256(f.read()).hexdigest()
        with open(self.audit_file, "r") as f:
            saved_hash = f.read()
        return current_hash == saved_hash
=======
        return txn_id
>>>>>>> 90f26134e12423dae4455a9bd4164f27843b7d4c
