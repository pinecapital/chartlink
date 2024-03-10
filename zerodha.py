from kiteconnect import KiteConnect
import config_loader
import token_manager
import authenticator

config = config_loader.load_config('config.json')
kite = KiteConnect(api_key=config['api_key'])

token_file_path = 'token.config'
access_token = token_manager.load_access_token(token_file_path)

if access_token is None:
    print("No valid token found. Authenticating...")
    access_token = authenticator.authenticate_and_get_token(kite, token_file_path, token_manager)
else:
    print("Using saved access token.")

kite.set_access_token(access_token)
print(kite.profile())
