from kiteconnect import KiteConnect
import config_loader
import token_manager
import authenticator
import instruments_manager
import json
from jsonEncoder import CustomJSONEncoder


config = config_loader.load_config('config.json')
kite = KiteConnect(api_key=config['api_key'])

token_file_path = 'token.config'
access_token = token_manager.load_access_token(token_file_path)

if access_token is None:
    print("No valid token found. Authenticating...")
    access_token = authenticator.authenticate_and_get_token(kite, token_file_path, token_manager)
else:
    print("Using saved access token.")

def get_last_price(symbol):
    return kite.quote(f"NSE:{symbol}")[f"NSE:{symbol}"]['last_price']

def get_atm_option_symbol(symbol, option_type):
    current_price = get_last_price(symbol)
    instruments_df = instruments_manager.read_instruments_to_dataframe('instruments.json')
    atm_options_df = instruments_manager.filter_options(instruments_df, symbol, option_type, current_price)
    
    if not atm_options_df.empty:
        atm_option = atm_options_df.iloc[0]
        trading_symbol = atm_option['tradingsymbol']
        lot_size = atm_option['lot_size']
        return trading_symbol, lot_size
    else:
        print(f"No ATM option found for {symbol} with type {option_type}")
        return None, None



kite.set_access_token(access_token)
# Download instruments data
# print("downloading instruments data...")
# instruments = kite.instruments()
# instruments_file_path = 'instruments.json'
# with open(instruments_file_path, 'w') as file:
#     json.dump(instruments, file, cls=CustomJSONEncoder)  

# print(f"Instruments data saved to {instruments_file_path}.")


# Example usage
atm_option_symbol, lot_size = get_atm_option_symbol('PAGEIND', 'CE')
if atm_option_symbol and lot_size:
    print(f"ATM Option Symbol: {atm_option_symbol}, Lot Size: {lot_size}")
    # You can now use atm_option_symbol and lot_size in your order placement function
    # place_order(atm_option_symbol, lot_size)
