import pandas as pd

def read_instruments_to_dataframe(file_path):
    return pd.read_json(file_path)

def filter_options(instruments_df, symbol, option_type, current_price):
    instruments_df['expiry'] = pd.to_datetime(instruments_df['expiry'])
    current_year = pd.Timestamp.now().year
    current_month = pd.Timestamp.now().month

    options_df = instruments_df[(instruments_df['expiry'].dt.year == current_year) &
                                (instruments_df['name'] == symbol) &
                                (instruments_df['expiry'].dt.month == current_month) &
                                (instruments_df['instrument_type'] == option_type)].copy()

    options_df['strike_diff'] = (options_df['strike'] - current_price).abs()
    atm_strike = options_df.loc[options_df['strike_diff'].idxmin(), 'strike']
    
    return options_df[options_df['strike'] == atm_strike]
