from behave import *
from pages import HomePage
from pages import PaymentPage
import time

use_step_matcher('re')

@given(r'I make a booking from "(?P<from_airport>[A-Z]{3})"'
        ' to "(?P<to_airport>[A-Z]{3})"'
        ' on (?P<date>\d{2}/\d{2}/\d{4})'
        ' for (?P<adults>\d+) adults?'
        ' and (?P<children>\d+) child(?P<pl>ren)?')
def make_booking(context, from_airport, to_airport, date, adults, children, pl):
    home_page = HomePage(context.browser)
    home_page.close_cookie_policy()
    home_page.select_one_way()
    home_page.set_airport_from(from_airport)
    home_page.set_airport_to(to_airport)
    home_page.set_date(date)
    home_page.set_passengers(adults=adults, children=children)
    search_page = home_page.press_lets_go()
    # there is a promo popup for families if there's at least one child
    if children > 0:
        search_page.close_promo_popup()
    search_page.choose_first_flight_regular_price()
    #this is an ugly hack but for some reason I get "checkout took too long"
    # if I press continue too fast
    time.sleep(1)
    extras_page = search_page.press_continue()
    extras_page.press_check_out()
    context.payment_page = extras_page.close_seat_popup()

@when(r'I pay for booking'
        ' with card details "(?P<number>\d{4}\s?\d{4}\s?\d{4}\s?\d{4})"'
        ', "(?P<date>\d{2}/\d{2})"'
        ' and "(?P<cvv>\d{3})"')
def pay_with_card(context, number, date, cvv):
    payment_page = context.payment_page
    payment_page.fill_passenger_data()
    payment_page.fill_contact_details()
    payment_page.fill_card_details(number, date, cvv)
    payment_page.fill_billing_address()
    payment_page.accept_terms()
    payment_page.press_pay_now()

@then('I should get payment declined message')
def check_payment_declined(context):
    context.payment_page.check_payment_declined()
