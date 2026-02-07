import hashlib
import json
import time
import os

LOG_FILE = "audit_log.jsonl"

class AuditLogger:
    def __init__(self, log_file=LOG_FILE):
        self.log_file = log_file
        self.last_hash = "0" * 64
        if os.path.exists(self.log_file):
            with open(self.log_file, "r") as f:
                lines = f.readlines()
                if lines:
                    last_entry = json.loads(lines[-1])
                    self.last_hash = last_entry["hash"]

    def log_transaction(self, data):
        timestamp = time.time()
        entry = {
            "timestamp": timestamp,
            "data": data,
            "previous_hash": self.last_hash
        }
        
        # Create a hash of the current entry
        entry_string = json.dumps(entry, sort_keys=True).encode()
        current_hash = hashlib.sha256(entry_string).hexdigest()
        entry["hash"] = current_hash
        
        with open(self.log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")
        
        self.last_hash = current_hash
        return current_hash

if __name__ == "__main__":
    logger = AuditLogger()
    h = logger.log_transaction({"event": "PII_REDACTION", "details": "Redacted email from request"})
    print(f"Logged transaction with hash: {h}")
