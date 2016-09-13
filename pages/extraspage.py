from basepage import BasePage
from paymentpage import PaymentPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ExtrasPage(BasePage):

    def __init__(self, browser):
        BasePage.__init__(self, browser)
        # Wait for the last section to be loaded - then it's safe to click
        WebDriverWait(self.browser, self.wait_time).until(
            EC.visibility_of_element_located(
                (By.CLASS_NAME, 'section-equipment')))

    def press_check_out(self):
        check_out_button = self.browser.find_element_by_css_selector(
            'div.trips-basket > button')
        check_out_button.click()

    def close_seat_popup(self):
        selector = 'button[ng-click="closeThisDialog()"]'
        WebDriverWait(self.browser, self.wait_time).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
        popup_close_button = self.browser.find_element_by_css_selector(selector)
        popup_close_button.click()
        return PaymentPage(self.browser)
