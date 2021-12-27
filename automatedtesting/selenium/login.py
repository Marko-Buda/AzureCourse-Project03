# #!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.common.exceptions import NoSuchElementException
import logging
import sys

shopping_list = [
    "sauce-labs-backpack",
    "sauce-labs-bike-light",
    "sauce-labs-bolt-t-shirt",
    "sauce-labs-fleece-jacket",
    "sauce-labs-onesie",
    "test.allthethings()-t-shirt-(red)",
]


def custom_logging_creation():
    mainLogger = logging.getLogger()

    logFormatter = logging.Formatter(fmt="%(asctime)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    fileHandler = logging.FileHandler(
        filename="selenium-report.txt",
    )
    fileHandler.setFormatter(logFormatter)

    consoleHandler = logging.StreamHandler(stream=sys.stdout)
    consoleHandler.setFormatter(logFormatter)
    mainLogger.setLevel(logging.INFO)

    mainLogger.addHandler(fileHandler)
    mainLogger.addHandler(consoleHandler)

    return mainLogger


# Start the browser and login with standard_user
def login(user, password):
    mainLogger.info("Starting the browser...")
    # --uncomment when running in Azure DevOps.
    options = ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    driver = webdriver.Chrome('/usr/bin/chromedriver', options=options)

    mainLogger.info("Browser started successfully. Navigating to the demo page to login.")
    driver.get("https://www.saucedemo.com/")

    mainLogger.info("Entering login credentials.")
    driver.find_element_by_css_selector("input[id='user-name']").send_keys(user)
    driver.find_element_by_css_selector("input[id='password']").send_keys(password)
    driver.find_element_by_css_selector("input[id='login-button']").click()

    login_status = driver.find_element_by_css_selector(
        "div[id='header_container'] > div[class='header_secondary_container'] > span.title"
    ).text
    assert "PRODUCTS" in login_status
    mainLogger.info("Succesfully logged into demo page with user %s" % user)

    return driver


def add_all_items_to_cart(driver):
    mainLogger.info("Started adding items to the cart.")
    for shopping_item in shopping_list:
        filtered_shopping_item = shopping_item.replace("-", " ").lower()
        mainLogger.info("Adding item '%s' to cart." % filtered_shopping_item)
        driver.find_element_by_css_selector("button[id='add-to-cart-%s']" % (shopping_item)).click()
    mainLogger.info("Finished adding items to the cart.")


def check_products_in_cart(driver):
    mainLogger.info("Check that all items were added to the cart.")
    number_of_item_in_cart = driver.find_element_by_css_selector(
        "div[id='shopping_cart_container'] > a > span.shopping_cart_badge"
    ).text
    assert 6 == int(number_of_item_in_cart)
    mainLogger.info("All items were successfully added to the cart.")


def remove_all_items_from_cart(driver):
    mainLogger.info("Started removing items from the cart.")
    for shopping_item in shopping_list:
        filtered_shopping_item = shopping_item.replace("-", " ").lower()
        mainLogger.info("Removing item '%s' from cart." % filtered_shopping_item)
        driver.find_element_by_css_selector("button[id='remove-%s']" % (shopping_item)).click()
    mainLogger.info("Finished removing items from the cart.")


def check_no_products_in_cart(driver):
    mainLogger.info("Check that all items were removed from the cart.")
    try:
        driver.find_element_by_css_selector("div[id='shopping_cart_container'] > a > span.shopping_cart_badge").text
    except NoSuchElementException:
        mainLogger.info("All items were successfully removed from the cart.")
    else:
        sys.exit("Error, not all items were removed from cart!")
    finally:
        driver.quit()


if __name__ == "__main__":
    mainLogger = custom_logging_creation()
    driver = login("standard_user", "secret_sauce")
    add_all_items_to_cart(driver)
    check_products_in_cart(driver)
    remove_all_items_from_cart(driver)
    check_no_products_in_cart(driver)
