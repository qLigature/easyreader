import os
import time
import yaml
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains

# Load config values from YAML file

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

targeturl = "https://myeasytripcams.easytrip.ph/CAMS/"
username = config["easytrip"]["credentials"]["username"]
password = config["easytrip"]["credentials"]["password"]
wait_time = config["selenium"]["wait-time"]
wait_time_download = config["selenium"]["wait-time-download"]
target_date = "03/20/2022"

if config["easytrip"]["downloadpath"] == None:
    downloadpath = os.getcwd()
else:
    downloadpath = config["easytrip"]["downloadpath"]

# Instantiate browser
chromedriver_autoinstaller.install()

chromeOptions = webdriver.ChromeOptions()
prefs = {"plugins.always_open_pdf_externally": True}
chromeOptions.add_experimental_option("prefs", prefs)
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

# Select first plate number to appear
search_dropdown = driver.find_element(By.ID, "tbSOASearchCriteria")
search_dropdown.click()
dropdown = Select(search_dropdown)
dropdown.select_by_visible_text("Plate No")

plate_dropdown = driver.find_element(By.ID, "tbSOAPlateNo")
plate_dropdown.click()
dropdown = Select(plate_dropdown)
dropdown.select_by_index(1)

# Select SOA Type
report_dropdown = driver.find_element(By.ID, "tbRptType")
report_dropdown.click()
dropdown = Select(report_dropdown)
dropdown.select_by_visible_text("SOA")

# Select by day
range_dropdown = driver.find_element(By.ID, "tbDateRange")
range_dropdown.click()
dropdown = Select(range_dropdown)
dropdown.select_by_visible_text("By Day")

# Input target date for downloading
date_field = driver.find_element(By.ID, "SOADate")
date_field.send_keys(target_date)

# Refocus to generate button using Action Chains
actions = ActionChains(driver)
generate_btn = driver.find_element(By.CSS_SELECTOR, ".btn.btn-fill.btn-info")
actions.move_to_element(generate_btn)
actions.perform()
generate_btn.click()

time.sleep(wait_time_download)