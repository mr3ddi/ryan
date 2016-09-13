import sys
import os
from selenium import webdriver
from pages import HomePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def before_scenario(context, scenario):
    options = webdriver.ChromeOptions()
    options.add_argument("--kiosk")
    chromedriver_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'chromedriver'))
    print (chromedriver_path)
    context.browser = webdriver.Chrome(executable_path=chromedriver_path, chrome_options=options)
    context.browser.implicitly_wait(10)
    context.browser.get(HomePage.address)
    #WebDriverWait(context.browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.col-departure-airport')))

def after_scenario(context, scenario):
    context.browser.quit()
