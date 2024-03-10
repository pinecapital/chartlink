from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

# Setup WebDriver with webdriver_manager
driver = webdriver.Chrome(ChromeDriverManager().install())
