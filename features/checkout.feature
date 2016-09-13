Feature: Booking on Ryanair page

    Scenario: Booking up to a declined payment
        Given I make a booking from "DUB" to "SXF" on 29/09/2016 for 2 adults and 1 child
        When I pay for booking with card details "5555 5555 5555 5557", "10/18" and "265"
        Then I should get payment declined message
