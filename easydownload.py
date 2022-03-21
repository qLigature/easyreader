import yaml
from selenium import webdriver
import chromedriver_autoinstaller
import os

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

chromedriver_autoinstaller.install()

targeturl = "https://myeasytripcams.easytrip.ph/CAMS/"
username = config["easytrip"]["credentials"]["username"]
password = config["easytrip"]["credentials"]["password"]
downloadpath = os.getcwd() if config["easytrip"]["downloadpath"] == None else config["easytrip"]["downloadpath"]

# Instantiate browser
chromeOptions=webdriver.ChromeOptions()
prefs = {"plugins.always_open_pdf_externally": True}
chromeOptions.add_experimental_option("prefs",prefs)
params = {"behavior": "allow", "downloadPath": downloadpath}
driver = webdriver.Chrome(chrome_options=chromeOptions)
driver.execute_cdp_cmd("Page.setDownloadBehavior", params)

driver.get(targeturl)
