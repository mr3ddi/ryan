from basepage import BasePage
from extraspage import ExtrasPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class SearchPage(BasePage):

    def __init__(self, browser):
        BasePage.__init__(self, browser)
        # Wait for the last section to be loaded - then it's safe to click
        WebDriverWait(self.browser, self.wait_time).until(
            EC.visibility_of_element_located(
                (By.CLASS_NAME, 'flight-prices')))

    def choose_first_flight_regular_price(self):
        price_row = self.browser.find_elements_by_class_name('flight')[0]
        regular_price = price_row.find_element_by_class_name('regular')
        regular_price.click()

    def press_continue(self):
        # Wait for continue button to be clickable
        WebDriverWait(self.browser, self.wait_time).until(
            EC.element_to_be_clickable((By.ID, 'continue')))
        # Click continue
        continue_button = self.browser.find_element_by_id('continue')
        continue_button.click()
        return ExtrasPage(self.browser)
