import os
import time
import yaml
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime, timedelta


def get_target_date():
    # Get a valid date for downloading SOA
    input_date = input(
        "Enter target SOA date, in MM/DD/YYYY format. Leave blank to download yesterday's SOA: ")
    if input_date == "":
        yesterday = datetime.today() - timedelta(days=1)
        return yesterday.strftime("%m/%d/%Y")
    try:
        target_date = datetime.strptime(input_date, "%m/%d/%Y")
        return target_date.strftime("%m/%d/%Y")
    except:
        print("Error: Failed to process invalid value. Try again.")
        print("-"*20)
        return get_target_date()


def initialize_browser():
    # Initialize automatic browser
    chromedriver_autoinstaller.install()

    chromeOptions = webdriver.ChromeOptions()
    prefs = {"plugins.always_open_pdf_externally": True}
    chromeOptions.add_experimental_option("prefs", prefs)
    params = {"behavior": "allow", "downloadPath": downloadpath}
    driver = webdriver.Chrome(chrome_options=chromeOptions)
    driver.execute_cdp_cmd("Page.setDownloadBehavior", params)

    return driver


def log_in(driver):
    # Input credentials and log in
    username_field = driver.find_element(By.NAME, "UserName")
    password_field = driver.find_element(By.NAME, "Password")
    login_footer = driver.find_element(By.CLASS_NAME, "card-footer")
    login_button = login_footer.find_element(By.TAG_NAME, "button")

    username_field.send_keys(username)
    password_field.send_keys(password)
    login_button.click()

    time.sleep(wait_time)


def generate_soa(driver):
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
    generate_btn = driver.find_element(
        By.CSS_SELECTOR, ".btn.btn-fill.btn-info")
    actions.move_to_element(generate_btn)
    actions.perform()
    generate_btn.click()

    time.sleep(wait_time_download)


# Load config values from YAML file
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

username = config["easytrip"]["username"]
password = config["easytrip"]["password"]
wait_time = config["selenium"]["wait-time"]
wait_time_download = config["selenium"]["wait-time-download"]
downloadpath = os.getcwd() + "\\pdf"

# Get target SOA date
target_date = get_target_date()
parsed_date = datetime.strptime(target_date, "%m/%d/%Y")
output_filename = "./pdf/" + parsed_date.strftime("%Y%m%d") + ".pdf"

driver = initialize_browser()

# Go to Easytrip login
target_url = "https://myeasytripcams.easytrip.ph/CAMS/"
driver.get(target_url)

# Interact with website and download a PDF
log_in(driver)
generate_soa(driver)

# Rename downloaded file and print status
try:
    os.rename("./pdf/SOAViewer.pdf", output_filename)
    print("PDF file successfully downloaded.")
    driver.quit()

except:
    print("Error! Skipping download because either (1) the download failed, or (2) the file you are trying to download already exists.")
    input("Press any key to continue...")
