from basepage import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class PaymentPage(BasePage):

    def __init__(self, browser):
        BasePage.__init__(self, browser)
        WebDriverWait(self.browser, self.wait_time).until(
            EC.visibility_of_element_located((By.ID, 'pay-now-btn')))

    def fill_passenger_data(self):
        actions = ActionChains(self.browser)
        title_selects = self.browser.find_elements_by_css_selector(
            'select[id^="title"]')

        # Go through all title select fields and set title to Mr
        # Yay for a stag party ;)
        for select_element in title_selects:
            actions.move_to_element(select_element)
            select = Select(select_element)
            select.select_by_index(1)

        first_names = self.browser.find_elements_by_css_selector(
            'input[id^="firstName"')
        for first_name in first_names:
            actions.move_to_element(first_name)
            first_name.send_keys("John")

        last_names = self.browser.find_elements_by_css_selector(
            'input[id^="lastName"')
        for idx, last_name in enumerate(last_names):
            actions.move_to_element(last_name)
            last_name.send_keys("Doe " + chr(idx + ord('a')))
