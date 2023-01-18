import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep
from random import random
from urllib.parse import urlencode
from car import Car
from advertisement import Advertisement


class AutopliusScraper:
    url = 'https://autoplius.lt/'

    def __init__(self):
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'

        options = Options()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument("--headless")
        options.add_argument("--incognito")
        options.add_argument(f'user-agent={user_agent}')

        print('Starting Chrome webdriver...')
        self.driver = webdriver.Chrome(options=options)

    def scrape_ads(self, num_of_ads, param=None):
        ads_url = self.url + 'skelbimai/naudoti-automobiliai'

        makes = self.scrape_makes()

        page = 1
        scraped_ads = []
        while len(scraped_ads) < num_of_ads:
            if param == None:
                param = dict()
            param['page_nr'] = page
            # param['make_id'] = make_id
            # param['model_id'] = model_id

            page_url = ads_url + '?' + urlencode(param)

            print(f'Scraping page #{page} - {page_url}')
            self.driver.get(page_url)
            self.driver.implicitly_wait(2)

            ads_parent = self.driver.find_element(
                By.CSS_SELECTOR, ".auto-lists.lt")

            self.driver.implicitly_wait(0)

            ads = ads_parent.find_elements(By.TAG_NAME, 'a')
            ads_urls = []
            for ad in ads:
                ads_urls.append(ad.get_attribute('href'))

            if (len(ads) == 0):
                print('No advertisements found.')
                break

            for ad_url in ads_urls:
                time1 = time.time()
                #sleep(random() * 3)

                self.driver.get(ad_url)

                try:
                    ad_id = WebDriverWait(self.driver, timeout=5).until(lambda d: d.find_element(
                        By.CSS_SELECTOR, "a.add-to-bookmark").get_attribute("data-id"))
                except Exception:
                    continue

                ad_title = self.driver.find_element(
                    By.XPATH, '//div[contains(@class, \'page-title\')]/h1').text.strip()

                print(ad_title)

                img_url = self.driver.find_element(By.CLASS_NAME, 'thumbnail').find_element(
                    By.TAG_NAME, 'img').get_attribute('src')

                price = self.driver.find_element(
                    By.CLASS_NAME, 'price').text.replace(' ', '')[:-1]

                for i in makes:
                    if ad_title.find(i) != -1:
                        make = i
                        ad_title = ad_title.removeprefix(make).strip()
                        break

                model = ad_title.split(',')[0]

                # Refactor this to loop from list of parameter names
                # Returns hashtable with parameter name and value
                production_date = self.driver.find_element(
                    By.XPATH, '//div[normalize-space()=\'Pagaminimo data\']/..')\
                    .find_element(By.CLASS_NAME, 'parameter-value')\
                    .text\
                    .strip()
                if len(production_date.split('-')) == 1:
                    production_date = production_date + "-01-01"
                elif len(production_date.split('-')) == 2:
                    production_date = production_date + "-01"

                mileage = self.driver.find_element(
                    By.XPATH, '//div[normalize-space()=\'Rida\']/..')\
                    .find_element(By.CLASS_NAME, 'parameter-value')\
                    .text\
                    .replace(' ', '')\
                    .removesuffix('km')

                enginecm3 = None
                enginehp = None
                if self.driver.find_elements(
                        By.XPATH, '//div[normalize-space()=\'Variklis\']/..'):
                    engine = self.driver.find_element(
                        By.XPATH, '//div[normalize-space()=\'Variklis\']/..')\
                        .find_element(By.CLASS_NAME, 'parameter-value')\
                        .text\
                        .strip()
                    if engine.find('cm') != -1:
                        enginecm3 = engine.split(' ')[0]
                        if engine.find('AG') != -1:
                            enginehp = engine.split(' ')[2]
                    else:
                        if engine.find('AG') != -1:
                            enginehp = engine.split(' ')[0]

                fuel_type = self.driver.find_element(
                    By.XPATH, '//div[normalize-space()=\'Kuro tipas\']/..')\
                    .find_element(By.CLASS_NAME, 'parameter-value')\
                    .text\
                    .strip()

                body_type = self.driver.find_element(
                    By.XPATH, '//div[normalize-space()=\'Kėbulo tipas\']/..')\
                    .find_element(By.CLASS_NAME, 'parameter-value')\
                    .text\
                    .strip()

                door_count = self.driver.find_element(
                    By.XPATH, '//div[normalize-space()=\'Durų skaičius\']/..')\
                    .find_element(By.CLASS_NAME, 'parameter-value')\
                    .text\
                    .strip()

                drivetrain = None
                if self.driver.find_elements(
                        By.XPATH, '//div[normalize-space()=\'Varantieji ratai\']/..'):
                    drivetrain = self.driver.find_element(
                        By.XPATH, '//div[normalize-space()=\'Varantieji ratai\']/..')\
                        .find_element(By.CLASS_NAME, 'parameter-value')\
                        .text\
                        .strip()

                transmission = self.driver.find_element(
                    By.XPATH, '//div[normalize-space()=\'Pavarų dėžė\']/..')\
                    .find_element(By.CLASS_NAME, 'parameter-value')\
                    .text\
                    .strip()

                color = None
                if self.driver.find_elements(
                        By.XPATH, '//div[normalize-space()=\'Spalva\']/..'):
                    color = self.driver.find_element(
                        By.XPATH, '//div[normalize-space()=\'Spalva\']/..')\
                        .find_element(By.CLASS_NAME, 'parameter-value')\
                        .text\
                        .strip()

                steering = self.driver.find_element(
                    By.XPATH, '//div[normalize-space()=\'Vairo padėtis\']/..')\
                    .find_element(By.CLASS_NAME, 'parameter-value')\
                    .text\
                    .strip()

                seat_count = None
                if self.driver.find_elements(
                        By.XPATH, '//div[normalize-space()=\'Sėdimų vietų skaičius\']/..'):
                    seat_count = self.driver.find_element(
                        By.XPATH, '//div[normalize-space()=\'Sėdimų vietų skaičius\']/..')\
                        .find_element(By.CLASS_NAME, 'parameter-value')\
                        .text\
                        .strip()

                car = Car(
                    make=make,
                    model=model,
                    production_date=production_date,
                    mileage=mileage,
                    engine=enginecm3,
                    horse_power=enginehp,
                    seat_count=seat_count,
                    fuel_type=fuel_type,
                    body_type=body_type,
                    door_count=door_count,
                    drivetrain=drivetrain,
                    transmission=transmission,
                    color=color,
                    steering=steering,
                )

                advertisement = Advertisement(
                    id=ad_id,
                    website_name='Autoplius',
                    ad_url=ad_url,
                    photo_url=img_url,
                    price=price,
                    car=car
                )

                print(advertisement)

                scraped_ads.append(car)

                time2 = time.time()
                print(f'Time spent on ad: {time2 - time1}')

                if (len(scraped_ads) >= num_of_ads):
                    break

            print(f'Scraped {len(scraped_ads)}/{num_of_ads} ads.')
            sleep(random() * 3)
            page = page + 1

        print(f'Scraping done. ({len(scraped_ads)} ads scraped)')

        return scraped_ads

    def scrape_makes(self):
        print('Scraping makes...')
        self.driver.get(self.url)
        self.driver.implicitly_wait(5)

        dropdown_options = self.driver.find_element(
            By.CSS_SELECTOR, '.form-row.make-and-model-row')\
            .find_element(By.CSS_SELECTOR, '.form-col.form-col-2')\
            .find_elements(By.CSS_SELECTOR, '.dropdown-option.js-option')

        makes = []
        for option in dropdown_options:
            make = option.get_attribute('data-title')
            makes.append(make)

        print(f'Scraping done. ({len(makes)} makes found)')
        return makes

    def quit_driver(self):
        self.driver.quit()
        print('Quitting webdriver...')
