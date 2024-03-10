import pyotp
import json
import os
import time
# Read the secret key from the config.json file in the previous folder
with open(os.path.join(os.path.dirname(__file__), '..', 'config.json')) as f:
    config = json.load(f)
    key = config['totp']

totp = pyotp.TOTP(key)
print(totp.now())
# Calculate and print the remaining time for the OTP
remaining_time = 30 - int(time.time()) % 30
print(f"Remaining time: {remaining_time} seconds")