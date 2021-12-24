# #!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.common.exceptions import NoSuchElementException

# Start the browser and login with standard_user
def login (user, password):
    shopping_list = [
        "sauce-labs-backpack",
        "sauce-labs-bike-light",
        "sauce-labs-bolt-t-shirt",
        "sauce-labs-fleece-jacket",
        "sauce-labs-onesie",
        "test.allthethings()-t-shirt-(red)"
    ]
    print ('Starting the browser...')
    # --uncomment when running in Azure DevOps.
    # options = ChromeOptions()
    # options.add_argument("--headless")
    # driver = webdriver.Chrome(options=options)
    driver = webdriver.Chrome('/usr/local/bin/chromedriver')

    print ('Browser started successfully. Navigating to the demo page to login.')
    driver.get('https://www.saucedemo.com/')

    print ('Entering login credentials.')
    driver.find_element_by_css_selector("input[id='user-name']").send_keys(user)
    driver.find_element_by_css_selector("input[id='password']").send_keys(password)
    driver.find_element_by_css_selector("input[id='login-button']").click()

    login_status = driver.find_element_by_css_selector("div[id='header_container'] > div[class='header_secondary_container'] > span.title").text
    assert "PRODUCTS" in login_status
    print ('Succesfully logged into demo page.')

    for shopping_item in shopping_list:
        driver.find_element_by_css_selector("button[id='add-to-cart-%s']" % (shopping_item)).click()

    number_of_item_in_cart = driver.find_element_by_css_selector("div[id='shopping_cart_container'] > a > span.shopping_cart_badge").text
    assert 6 == int(number_of_item_in_cart)
    print("All items were successfully added to the cart.")

    for shopping_item in shopping_list:
        driver.find_element_by_css_selector("button[id='remove-%s']" % (shopping_item)).click()

    try:
        driver.find_element_by_css_selector("div[id='shopping_cart_container'] > a > span.shopping_cart_badge").text
    except NoSuchElementException:
        print("All items were successfully removed from the cart.")
    return driver.close()

login('standard_user','secret_sauce')
