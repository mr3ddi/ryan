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
        container_id = 'search-container'
        WebDriverWait(self.browser, self.wait_time).until(
            EC.visibility_of_element_located((By.ID, container_id)))
        self.__search_form = self.browser.find_element_by_id(container_id)

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
        # Make sure date input fields are visible
        WebDriverWait(self.browser, self.wait_time).until(
            EC.visibility_of_element_located((By.NAME, 'dateInput2')))

        # Set value for each field (day, month, year)
        for idx, value in enumerate(date.split('/')):
            field = self.__search_form.find_element_by_name(
                'dateInput' + str(idx))

            # Check if we want to set a different value than the one that is
            # in the field already
            if field.text != value:
                field.clear()
                field.send_keys(value)

    def close_cookie_policy(self):
        close_button = self.browser.find_element_by_class_name('close-icon')
        close_button.click()

    def set_passengers(self, **kwargs):
        total = 0
        dropdown = self.__search_form.find_element_by_class_name(
            'dropdown-handle')
        dropdown.click()

        # We get kwargs with names: adult, child - so we can enumerate them
        # and create selector dynamically
        for name, value in kwargs.iteritems():
            if value > 0:
                selector = 'div[value="paxInput.' + name + '"] input.num'
                # Wait for each input field before setting value
                WebDriverWait(self.browser, self.wait_time).until(
                    EC.visibility_of_element_located(
                        (By.CSS_SELECTOR, selector)))
                input = self.__search_form.find_element_by_css_selector(
                    selector)
                input.clear()
                input.send_keys(value)
                total += int(value)
                # Need to wait for the total passenger value to refresh
                # before setting next passenger group or it won't work
                WebDriverWait(self.browser, self.wait_time).until(
                    EC.text_to_be_present_in_element(
                        (By.CSS_SELECTOR, '#row-dates-pax div.value'),
                        str(total))
                )

    def press_lets_go(self, children):
        button = self.__search_form.find_element_by_css_selector(
            'button[ng-click="searchFlights()"]')
        button.click()
         # there is a promo popup for families if there's at least one child
        if children > 0:
            self.close_promo_popup()
        return SearchPage(self.browser)

    def close_promo_popup(self):
        class_ = 'promo-popup-close'
        # Wait for the popup to show up
        WebDriverWait(self.browser, self.wait_time).until(
            EC.visibility_of_element_located((By.CLASS_NAME, class_)))
        # Click close button
        close_button = self.browser.find_element_by_class_name(class_)
        close_button.click()
