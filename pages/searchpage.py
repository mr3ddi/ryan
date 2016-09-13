from basepage import BasePage
from extraspage import ExtrasPage

class SearchPage(BasePage):

    def choose_first_flight_regular_price(self):
        price_row = self.browser.find_elements_by_class_name('flight')[0]
        regular_price = price_row.find_element_by_class_name('regular')
        regular_price.click()

    def close_promo_popup(self):
        close_button = self.browser.find_element_by_class_name(
            'promo-popup-close')
        close_button.click()

    def press_continue(self):
        continue_button = self.browser.find_element_by_id('continue')
        continue_button.click()
        return ExtrasPage(self.browser)
