from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
from random import random

page = input('Which page do you want to explore?: ')

user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
options = Options()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--headless")
options.add_argument("--incognito")
options.add_argument(f'user-agent={user_agent}')

# Create a new Chrome webdriver
driver = webdriver.Chrome(options=options)

for i in range(10):
    # Load the web page
    url = 'https://autoplius.lt/skelbimai/naudoti-automobiliai?page_nr=' + \
        str(i)
    #driver.get('https://autoplius.lt/skelbimai/naudoti-automobiliai?make_id=97&model_id=1313&body_type_id%5B4%5D=4&page_nr=' + page)
    driver.get(url)

    # Wait for the page to be loaded
    driver.implicitly_wait(5)

    print(driver.title)

    items = driver.find_elements("class name", "announcement-item")
    print("Found", len(items), "items")

    # driver.get_screenshot_as_file("screenshot.png")

    driver.implicitly_wait(0)
    for item in items:
        name = item.find_element("class name", "announcement-title")
        city = item.find_elements("xpath", ".//span[@title='Miestas']")
        id = item.find_element(
            "class name", "announcement-bookmark-button ").get_attribute("data-id")

        if len(city) > 0:
            print(name.text, city[0].text, id)

    sleep(random() * 3)

print("Scraping done.")

# Close the webdriver
driver.quit()

print("Driver was stopped.")

# user agent Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36
# referer https://autoplius.lt/skelbimai/alfa-romeo-crosswagon-q4-1-9-l-universalas-2005-dyzelinas-22685200.html

# Execute JavaScript to extract the content you want to scrape
# content = driver.execute_script('return document.documentElement.outerHTML')
