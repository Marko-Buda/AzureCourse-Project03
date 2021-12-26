# #!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.common.exceptions import NoSuchElementException
import logging
import sys

# Start the browser and login with standard_user
def login (user, password):
    logging.basicConfig(filename="selenium-report.txt",
                        format="%(asctime)-4s %(message)s",
                        stream=sys.stdout,
                        filemode="w",
                        level=logging.INFO)
    shopping_list = [
        "sauce-labs-backpack",
        "sauce-labs-bike-light",
        "sauce-labs-bolt-t-shirt",
        "sauce-labs-fleece-jacket",
        "sauce-labs-onesie",
        "test.allthethings()-t-shirt-(red)"
    ]
    logging.info('Starting the browser...')
    # --uncomment when running in Azure DevOps.
    options = ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.setBinary("/usr/bin/chromium-browser")
    driver = webdriver.Chrome(options=options)
    #driver = webdriver.Chrome('/usr/local/bin/chromedriver')

    logging.info('Browser started successfully. Navigating to the demo page to login.')
    driver.get('https://www.saucedemo.com/')

    logging.info('Entering login credentials.')
    driver.find_element_by_css_selector("input[id='user-name']").send_keys(user)
    driver.find_element_by_css_selector("input[id='password']").send_keys(password)
    driver.find_element_by_css_selector("input[id='login-button']").click()

    login_status = driver.find_element_by_css_selector("div[id='header_container'] > div[class='header_secondary_container'] > span.title").text
    assert "PRODUCTS" in login_status
    logging.info('Succesfully logged into demo page.')

    logging.info("Adding items to the cart.")
    for shopping_item in shopping_list:
        driver.find_element_by_css_selector("button[id='add-to-cart-%s']" % (shopping_item)).click()

    number_of_item_in_cart = driver.find_element_by_css_selector("div[id='shopping_cart_container'] > a > span.shopping_cart_badge").text
    assert 6 == int(number_of_item_in_cart)
    logging.info("All items were successfully added to the cart.")

    logging.info("Removing items from the cart.")
    for shopping_item in shopping_list:
        driver.find_element_by_css_selector("button[id='remove-%s']" % (shopping_item)).click()

    try:
        driver.find_element_by_css_selector("div[id='shopping_cart_container'] > a > span.shopping_cart_badge").text
    except NoSuchElementException:
        logging.info("All items were successfully removed from the cart.")
    else: sys.exit("Error, not all items were removed from cart!")
    finally: driver.quit()

login('standard_user','secret_sauce')
