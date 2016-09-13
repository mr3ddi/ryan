# ryan

ryan is a simple UI test that checks if correct message is displayed for
declined payment.

It is written in python using
[Behave](https://pythonhosted.org/behave/)
for BDD and
[Selenium WebDriver](http://www.seleniumhq.org/)
for browser automation.

ChromeDriver is used as Chrome is the most popular browser in the world.

ryan finds elements by _id_ or _name_ wherever possible.
Unfortunately not all elements on Ryanair page have id or name.
In such cases ryan will use _class_ or even _css_ when simple _class_ name is
not available.

_id_, _name_ and _class_ are used for readability as they are implemented with
_css selector_ in Selenium Python bindings anyway ;)

Steps have no input error detection so please be aware of following
restrictions (taken from example test input) when changing feature file:

* Airport codes have to be written as 3 uppercase letters
* Flight date has to be in dd/mm/yyyy format
* Number of adults has to be a number
* Number of children has to be a number
* Card number can be in 'dddddddddddddddd' or 'dddd dddd dddd dddd' format
* Card expiry date has to be in mm/yy format
* CVV has to be a 3 digit number

For simplicity ryan is not checking Ryanair's restrictions on the maximum
number of adults or adults with children.

## Requirements

### MacOS

ryan uses a MacOS chromedriver executable.
It is bundled in the repo so no download is required.

### Python 2.x

Bundled by default with MacOS thus no special download should be required.

### behave package

Can be installed with:

```bash
pip install selenium
```

### selenium package

Can be installed with:

```bash
pip install behave
```

## How to run tests

Simply type:

```bash
behave
```

in repo top-level directory.

For a test report in junit format you can run tests like this:

```bash
behave --junit --junit-directory output_directory
```

## Test reports

An example junit test report for ryan would look like this:

```xml
<?xml version='1.0' encoding='UTF-8'?>
<testsuite errors="0" failures="0" name="checkout.Booking on Ryanair page" skipped="0" tests="1" time="19.335644"><testcase classname="checkout.Booking on Ryanair page" name="Booking up to a declined payment" status="passed" time="19.335644"><system-out>
<![CDATA[
@scenario.begin
  Scenario: Booking up to a declined payment
    Given I make a booking from "DUB" to "SXF" on 21/10/2016 for 2 adults and 1 child ... passed in 16.582s
    When I pay for booking with card details "5555 5555 5555 5557", "10/18" and "265" ... passed in 2.753s
    Then I should get payment declined message ... passed in 0.000s

@scenario.end
--------------------------------------------------------------------------------
]]>
</system-out></testcase></testsuite>
```

## Things that __can__ and __should__ be improved (aka TODO)

* Write proper method documentation
* Use UI Map to gather all locators in one place (or one place per page)
* Move magic numbers to constants
* Introduce more variation in booking data as Ryanair detects duplicate bookings
and displays a different error message for them
* Introduce better granulation in Page Objects (page components)
* Introduce some input error detection
* Add requirements.txt for easier pip install of required packages
* Use scenario outline to add more data to tests
* Investigate why sometimes Ryanair page says there are no flights for given
date when there are flights
* Investigate why 1 second sleep is needed before pressing continue on extras
page
