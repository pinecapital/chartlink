import json
from datetime import datetime, timedelta
import pytz

def is_token_expired(token_time):
    ist_timezone = pytz.timezone('Asia/Kolkata')
    reset_time = datetime.now(ist_timezone).replace(hour=6, minute=0, second=0, microsecond=0)
    if datetime.now(ist_timezone) < reset_time:
        reset_time -= timedelta(days=1)
    return token_time < reset_time

def save_access_token(file_path, access_token):
    data = {
        'access_token': access_token,
        'timestamp': datetime.now().timestamp()
    }
    with open(file_path, 'w') as file:
        json.dump(data, file)

def load_access_token(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            ist_timezone = pytz.timezone('Asia/Kolkata')
            token_time = datetime.fromtimestamp(data['timestamp'], tz=ist_timezone)
            if is_token_expired(token_time):
                return None
            return data['access_token']
    except FileNotFoundError:
        return None
