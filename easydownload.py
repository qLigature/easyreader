import yaml
from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
import os
import time

# Load config values from YAML file

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

targeturl = "https://myeasytripcams.easytrip.ph/CAMS/"
username = config["easytrip"]["credentials"]["username"]
password = config["easytrip"]["credentials"]["password"]
wait_time = config["selenium"]["wait-time"]
wait_time_download = config["selenium"]["wait-time-download"]

if config["easytrip"]["downloadpath"] == None:
    downloadpath = os.getcwd()
else:
    downloadpath = config["easytrip"]["downloadpath"]

# Instantiate browser
chromedriver_autoinstaller.install()

chromeOptions=webdriver.ChromeOptions()
prefs = {"plugins.always_open_pdf_externally": True}
chromeOptions.add_experimental_option("prefs",prefs)
params = {"behavior": "allow", "downloadPath": downloadpath}
driver = webdriver.Chrome(chrome_options=chromeOptions)
driver.execute_cdp_cmd("Page.setDownloadBehavior", params)

# Go to Easytrip login
driver.get(targeturl)

# Input credentials and log in
username_field = driver.find_element(By.NAME, "UserName")
password_field = driver.find_element(By.NAME, "Password")
login_footer = driver.find_element(By.CLASS_NAME, "card-footer")
login_button = login_footer.find_element(By.TAG_NAME, "button")

username_field.send_keys(username)
password_field.send_keys(password)
login_button.click()

time.sleep(wait_time)

# Go to Generate SOA
soa_card = driver.find_element(By.LINK_TEXT, "Generate SOA")
soa_card.click()

time.sleep(wait_time)

