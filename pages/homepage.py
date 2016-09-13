from basepage import BasePage
from searchpage import SearchPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class HomePage(BasePage):
    address = 'https://www.ryanair.com/ie/en/'

    def __init__(self, browser):
        BasePage.__init__(self, browser)
        self.__search_form = self.browser.find_element_by_id('search-container')

    def select_one_way(self):
        one_way_select = self.__search_form.find_element_by_id(
            'flight-search-type-option-one-way')
        one_way_select.click()

    def set_airport_from(self, airport):
        self.__set_airport('input[placeholder="Departure airport"]', airport)

    def set_airport_to(self, airport):
        self.__set_airport('input[placeholder="Destination airport"]', airport)

    def __set_airport(self, selector, airport):
        element = self.__search_form.find_element_by_css_selector(selector)
        element.click()
        element.send_keys(airport+'\t')

    def set_date(self, date):
        for idx, value in enumerate(date.split('/')):
            field = self.__search_form.find_element_by_name(
                'dateInput' + str(idx))
            if field.text != value:
                field.send_keys('\b\b' * idx + value)

    def close_cookie_policy(self):
        close_button = self.browser.find_element_by_class_name('close-icon')
        close_button.click()

    def set_passengers(self, **kwargs):
        total = 0
        dropdown = self.__search_form.find_element_by_class_name(
            'dropdown-handle')
        dropdown.click()
        for name, value in kwargs.iteritems():
            if value > 0:
                selector = 'div[value="paxInput.' + name + '"] input.num'
                input = self.__search_form.find_element_by_css_selector(
                    selector)
                input.click()
                input.send_keys(value)
                total += int(value)
                # Need to wait for the total passenger value to refresh
                # before setting next passenger group or it won't work
                WebDriverWait(self.browser, 5).until(
                    EC.text_to_be_present_in_element(
                        (By.CSS_SELECTOR, '#row-dates-pax div.value'),
                        str(total))
                )

    def press_lets_go(self):
        button = self.__search_form.find_element_by_css_selector(
            'button[ng-click="searchFlights()"]')
        button.click()
        return SearchPage(self.browser)
