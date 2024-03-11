from selenium import webdriver
from datetime import datetime
from kiteconnect import KiteConnect

def authenticate_and_get_token(kite, token_file_path, token_manager,api_secret):
    driver = webdriver.Chrome()
    login_url = kite.login_url()
    driver.get(login_url)
    input("Log in manually in the browser window and then press Enter here...")
    redirected_url = driver.current_url
    driver.quit()

    start = redirected_url.find('request_token=') + len('request_token=')
    end = redirected_url.find('&', start)
    request_token = redirected_url[start:end] if end != -1 else redirected_url[start:]
    data = kite.generate_session(request_token, api_secret)
    access_token = data["access_token"]
    token_manager.save_access_token(token_file_path, access_token)
    return access_token
