import sys
import os
from selenium import webdriver
from pages import HomePage

def before_scenario(context, scenario):
    options = webdriver.ChromeOptions()
    options.add_argument("--kiosk")
    chromedriver_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'chromedriver'))
    context.browser = webdriver.Chrome(
        executable_path=chromedriver_path) #, chrome_options=options)
    context.browser.implicitly_wait(10)
    context.browser.get(HomePage.address)

def after_scenario(context, scenario):
    context.browser.quit()
