from kiteconnect import KiteConnect
import config_loader
import token_manager
import authenticator
import instruments_manager
import json
from jsonEncoder import CustomJSONEncoder


config = config_loader.load_config('config.json')
api_secret = config['api_secret']
kite = KiteConnect(api_key=config['api_key'])

token_file_path = 'token.config'
access_token = token_manager.load_access_token(token_file_path)

if access_token is None:
    print("No valid token found. Authenticating...")
    access_token = authenticator.authenticate_and_get_token(kite, token_file_path, token_manager,api_secret)
else:
    print("Using saved access token.")

def get_last_price(symbol, exchange):
    full_symbol = f"{exchange}:{symbol}"
    return kite.quote(full_symbol)[full_symbol]['last_price']


def get_atm_option_symbol(symbol, option_type):
    current_price = get_last_price(symbol, 'NSE')
    instruments_df = instruments_manager.read_instruments_to_dataframe('instruments.json')
    atm_options_df = instruments_manager.filter_options(instruments_df, symbol, option_type, current_price)
    
    if not atm_options_df.empty:
        atm_option = atm_options_df.iloc[0]
        trading_symbol = atm_option['tradingsymbol']
        lot_size = atm_option['lot_size']
        tick_size = atm_option['tick_size']  # Fetch the tick size
        return trading_symbol, lot_size,tick_size
    else:
        print(f"No ATM option found for {symbol} with type {option_type}")
        return None, None


def adjust_to_tick_size(price, tick_size):
    return round(price / tick_size) * tick_size

kite.set_access_token(access_token)
# Download instruments data
# print("downloading instruments data...")
# instruments = kite.instruments()
# instruments_file_path = 'instruments.json'
# with open(instruments_file_path, 'w') as file:
#     json.dump(instruments, file, cls=CustomJSONEncoder)  

# print(f"Instruments data saved to {instruments_file_path}.")



def place_order(symbol, option_type):
    # Load order configurations
    with open('orderConfig.json', 'r') as file:
        order_config = json.load(file).get(symbol)

    if not order_config:
        print(f"Order configuration for {symbol} not found.")
        return

    qty_multiplier = order_config['qty_multiplier']
    tp_percentage = order_config['tp']
    sl_percentage = order_config['sl']

    # Get ATM option symbol and lot size
    atm_option_symbol, lot_size, tick_size = get_atm_option_symbol(symbol, option_type)

    if not atm_option_symbol or not lot_size:
        print("Cannot place order, ATM option symbol or lot size not found.")
        return

    # Get the last price of the ATM option symbol
    last_price_option = get_last_price(atm_option_symbol, 'NFO')

    # Calculate total quantity based on lot size and qty_multiplier
    total_qty = lot_size * qty_multiplier

    print(f"Placing limit order for {atm_option_symbol} with quantity {total_qty}")

    # For a buy limit order, you might set the limit price slightly above the last price to ensure execution
    limit_price = adjust_to_tick_size(last_price_option * (1 + 0.01), tick_size)  # 1% above as an example

    # Place limit order
    order_id = kite.place_order(tradingsymbol=atm_option_symbol,
                                exchange=kite.EXCHANGE_NFO,
                                transaction_type=kite.TRANSACTION_TYPE_BUY,
                                quantity=total_qty,
                                order_type=kite.ORDER_TYPE_LIMIT,
                                price=limit_price,
                                product=kite.PRODUCT_NRML,
                                variety=kite.VARIETY_REGULAR)

    print(f"Limit order placed. Order ID: {order_id}")

    # TP and SL logic remains the same; just ensure they are placed as limit orders with appropriate prices

     #Assume order_id is obtained from the above place_order call
    print(order_id)

    # Calculate target price and stop loss price based on percentages
    stop_loss_price = adjust_to_tick_size(last_price_option * (1 - sl_percentage / 100),tick_size)
    target_price = adjust_to_tick_size(last_price_option * (1 + tp_percentage / 100), tick_size)
    stop_loss_trigger_price = adjust_to_tick_size(last_price_option * (1 - sl_percentage / 100), tick_size)



    print(f"Target Price: {target_price}, Stop Loss Price: {stop_loss_price}")
    # Place Target Price (TP) limit order - to take profit
    tp_order_id = kite.place_order(tradingsymbol=atm_option_symbol,
                                   exchange=kite.EXCHANGE_NFO,
                                   transaction_type=kite.TRANSACTION_TYPE_SELL,
                                   quantity=total_qty,
                                   order_type=kite.ORDER_TYPE_LIMIT,
                                   price=target_price,
                                   product=kite.PRODUCT_NRML,
                                   variety=kite.VARIETY_REGULAR)
    print(f"TP Limit order placed. Order ID: {tp_order_id}")
    # Place Stop Loss (SL) order - to limit loss
    sl_order_id = kite.place_order(tradingsymbol=atm_option_symbol,
                                   exchange=kite.EXCHANGE_NFO,
                                   transaction_type=kite.TRANSACTION_TYPE_SELL,
                                   quantity=total_qty,
                                   order_type=kite.ORDER_TYPE_SL,
                                   trigger_price=stop_loss_trigger_price,  # For SL order, set trigger_price
                                   price=stop_loss_trigger_price - 1,  # Set price slightly lower than trigger for SL-Limit order
                                   product=kite.PRODUCT_NRML,
                                   variety=kite.VARIETY_REGULAR)
    print(f"SL Order placed. Order ID: {sl_order_id}")



place_order('SBIN', 'CE')
