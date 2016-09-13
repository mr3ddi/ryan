from basepage import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class PaymentPage(BasePage):

    def __init__(self, browser):
        BasePage.__init__(self, browser)
        # Wait for pay now button - then it's safe to click
        WebDriverWait(self.browser, self.wait_time).until(
            EC.visibility_of_element_located((By.ID, 'payment-contact-form')))

    def fill_passenger_data(self):
        title_selects = self.browser.find_elements_by_css_selector(
            'select[id^="title"]')

        # Go through all title select fields and set title to Mr
        for select_element in title_selects:
            select = Select(select_element)
            select.select_by_index(1)

        first_names = self.browser.find_elements_by_css_selector(
            'input[id^="firstName"')
        for first_name in first_names:
            first_name.send_keys("John")

        last_names = self.browser.find_elements_by_css_selector(
            'input[id^="lastName"')
        for idx, last_name in enumerate(last_names):
            last_name.send_keys("Doe " + chr(idx + ord('a')))

    def fill_contact_details(self):
        # Fill email and email confirmation fields
        for field in ('emailAddress', 'confirmEmail'):
            email_field = self.browser.find_element_by_name(field)
            email_field.send_keys('abc@abc.pl')

        # Set Poland as phone country
        country_select = self.browser.find_element_by_name('phoneNumberCountry')
        select = Select(country_select)
        select.select_by_index(27)

        # Fill phone number
        # Have to use actions to work around a bug in chromedriver - see:
        # https://bugs.chromium.org/p/chromedriver/issues/detail?id=35
        phone_input = self.browser.find_element_by_name('phoneNumber')
        actions = ActionChains(self.browser)
        actions.move_to_element(phone_input)
        actions.click()
        actions.send_keys('12345678')
        actions.perform()

    def fill_card_details(self, number, date, cvv):
        # Remove spaces from card number and fill card number field
        card_number = self.browser.find_element_by_name('cardNumber')
        card_number.send_keys(number.replace(' ', ''))

        # Select first card type from the list
        card_type = self.browser.find_element_by_name('cardType')
        select = Select(card_type)
        select.select_by_index(1)

        # Date is in \d{2}/\d{2} format so split it to month and year
        date = date.split('/')
        # Set expiry month
        expiry_month = self.browser.find_element_by_name('expiryMonth')
        select = Select(expiry_month)
        select.select_by_visible_text(date[0])
        # Set expiry year
        expiry_year = self.browser.find_element_by_name('expiryYear')
        select = Select(expiry_year)
        # We have last 2 digits of year so we have to prefix it with 20
        # This will work in this century only though
        select.select_by_visible_text("20" + date[1])

        # Fill CVV
        cvv_field = self.browser.find_element_by_name('securityCode')
        cvv_field.send_keys(cvv)

        # Fill card holder name
        card_holder = self.browser.find_element_by_name('cardHolderName')
        card_holder.send_keys('John Doe')

    def fill_billing_address(self):
        # Fill first address line
        address_line1 = self.browser.find_element_by_id(
            'billingAddressAddressLine1')
        address_line1.send_keys('Street')

        # Fill city
        city = self.browser.find_element_by_id('billingAddressCity')
        city.send_keys('City')

        # Fill Postcode
        postcode = self.browser.find_element_by_id('billingAddressPostcode')
        postcode.send_keys('12345')

    def accept_terms(self):
        terms = self.browser.find_element_by_name('acceptPolicy')
        terms.click()

    def press_pay_now(self):
        pay_now = self.browser.find_element_by_id('pay-now-btn')
        pay_now.click()

    def check_payment_declined(self):
        class_ = 'error'
        # Wait for error prompt to show up
        WebDriverWait(self.browser, self.wait_time).until(
            EC.visibility_of_element_located((By.CLASS_NAME, class_)))
        error_prompt = self.browser.find_element_by_class_name(class_)
        # Check if prompt has correct text set
        assert error_prompt.get_attribute('text').endswith('error_explain_declined')
