from datetime import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep
from random import random
from urllib.parse import urlencode
from car import Car


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
            print(page)
            print(type(param))
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

                ad_id = WebDriverWait(self.driver, timeout=5).until(lambda d: d.find_element(
                    By.CSS_SELECTOR, "a.add-to-bookmark").get_attribute("data-id"))

                # ad_id = WebDriverWait(self.driver, timeout=5).until(lambda d: d.find_element(
                #    By.XPATH, "//a[contains(@class, 'add-to-bookmark')]").get_attribute("data-id"))

                ad_title = self.driver.find_element(
                    By.XPATH, '//div[contains(@class, \'page-title\')]/h1').text.strip()

                print(ad_title)

                for i in makes:
                    if ad_title.find(i) != -1:
                        make = i
                        ad_title = ad_title.removeprefix(make).strip()
                        break

                model = ad_title.split(',')[0]

                # Refactor this to loop from list of parameter names
                # Returns hashtable with parameter name and value
                # param_rows = self.driver.find_elements(
                #    By.CLASS_NAME, 'parameter-row')
                param_rows = self.driver.find_elements(
                    By.XPATH, '//div[(@class=\'col-5\')]/div/div[contains(@class, \'parameter-row\')]')

                params = {}
                for parameter in param_rows:
                    param_name = parameter.find_elements(
                        By.CLASS_NAME, 'parameter-label')
                    if len(param_name) > 0:
                        param_name = param_name[0].text.strip()
                    else:
                        param_name = parameter.find_elements(
                            By.CLASS_NAME, 'parameter-label ')[0].text.strip()

                    param_value = parameter.find_elements(
                        By.CLASS_NAME, 'parameter-value')
                    if len(param_value) > 0:
                        param_value = param_value[0].text.strip()
                    else:
                        param_value = parameter.find_elements(
                            By.CLASS_NAME, 'parameter-value ')[0].text.strip()
                    # if param.find_elements(By.CLASS_NAME, 'parameter-label'):
                    #     param_name = param.find_element(
                    #         By.CLASS_NAME, 'parameter-label').text.strip()
                    # else:
                    #     param_name = param.find_element(
                    #         By.CLASS_NAME, 'parameter-label ').text.strip()

                    # if param.find_elements(By.CLASS_NAME, 'parameter-value'):
                    #     param_value = param.find_element(
                    #         By.CLASS_NAME, 'parameter-value').text.strip()
                    # else:
                    #     param_value = param.find_element(
                    #         By.CLASS_NAME, 'parameter-value ').text.strip()

                    params[param_name] = param_value

                enginecm3 = -1
                enginehp = -1
                if 'Variklis' in params:
                    if params['Variklis'].find('cm') != -1:
                        enginecm3 = params['Variklis'].split(' ')[0]
                        if params['Variklis'].find('AG') != -1:
                            enginehp = params['Variklis'].split(' ')[2]
                    else:
                        if params['Variklis'].find('AG') != -1:
                            enginehp = params['Variklis'].split(' ')[0]

                seat_count = params['Sėdimų vietų skaičius'] if 'Sėdimų vietų skaičius' in params else -1
                drivetrain = params['Varantieji ratai'] if 'Varantieji ratai' in params else ""
                color = params['Spalva'] if 'Spalva' in params else ""
                mileage = params['Rida'].replace(' ', '').removesuffix('km')

                car = Car(
                    id=-1,
                    make=make,
                    model=model,
                    production_date=datetime(2020, 1, 1),
                    mileage=mileage,
                    engine=enginecm3,
                    horse_power=enginehp,
                    seat_count=seat_count,
                    fuel_type=params['Kuro tipas'],
                    body_type=params['Kėbulo tipas'],
                    door_count=params['Durų skaičius'],
                    drivetrain=drivetrain,
                    transmission=params['Pavarų dėžė'],
                    color=color,
                    steering=params['Vairo padėtis'],
                )

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
