import os
import time
from datetime import datetime
import pandas as pd
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from Backend.ScraperPrototype import ScraperPrototype


class EscortalligatorScraper(ScraperPrototype):
    def __init__(self):
        super().__init__()
        self.driver = None

        self.cities = [
            "daytona",
            "fort lauderdale",
            "fort myers",
            "gainesville",
            "jacksonville",
            "keys",
            "miami",
            "ocala",
            "okaloosa",
            "orlando",
            "palm bay",
            "panama city",
            "pensacola",
            "bradenton",
            "space coast",
            "st. augustine",
            "tallahassee",
            "tampa",
            "treasure coast",
            "west palm beach",
            "jacksonville"
        ]
        self.city = ''
        self.state = 'florida'
        self.url = ''
        self.known_payment_methods = ['cashapp', 'venmo', 'zelle', 'crypto', 'western union', 'no deposit',
                                      'deposit', 'cc', 'card', 'credit card', 'applepay', 'cash']

        self.date_time = None
        self.scraper_directory = None
        self.screenshot_directory = None
        self.keywords = None

        # lists to store data and then send to csv file
        self.phone_number = []
        self.description = []
        self.location_and_age = []
        self.links = []
        self.post_identifier = []
        self.payment_methods_found = []

        # TODO other info needs to be pulled using regex?

    def get_cities(self):
        return self.cities

    def set_city(self, city):
        self.city = city.replace(' ', '').replace('.', '')

    def initialize(self, keywords):
        #set the keywords value
        self.read_keywords(keywords)

        self.date_time = str(datetime.today())[0:19].replace(' ', '_').replace(':', '-')

        # Format website URL based on state and city
        self.get_formatted_url()

        # Selenium Web Driver setup
        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome()

        # Open Webpage with URL
        self.open_webpage()

        # Find links of posts
        links = self.get_links()

        # Create directory for search data
        self.scraper_directory = f'escortalligator_{self.date_time}'
        os.mkdir(self.scraper_directory)

        # Create directory for search screenshots
        self.screenshot_directory = f'{self.scraper_directory}/screenshots'
        os.mkdir(self.screenshot_directory)

        # Get data from posts
        self.get_data(links)
        self.close_webpage()
        self.format_data_to_csv()

    def open_webpage(self):
        self.driver.implicitly_wait(10)
        self.driver.get(self.url)
        assert "Page not found" not in self.driver.page_source

    def close_webpage(self):
        self.driver.close()

    def get_links(self):
        # click on terms btn
        btn = self.driver.find_element(
            By.CLASS_NAME, 'button')
        btn.click()

        time.sleep(2)
        # click on 2nd terms btn
        btn = self.driver.find_element(
            By.CLASS_NAME, 'footer')
        btn.click()

        posts = self.driver.find_elements(
            By.CSS_SELECTOR, '#list [href]')
        links = [post.get_attribute('href') for post in posts]
        return links[::3]

    def get_formatted_url(self):
        self.url = f'https://escortalligator.com.listcrawler.eu/brief/escorts/usa/{self.state}/{self.city}/1'
        print(f"link: {self.url}")

    def get_data(self, links):
        links = set(links)
        counter = 0

        for link in links:
            print(link)

            # self.driver.implicitly_wait(10)
            # time.sleep(3)
            self.driver.get(link)
            assert "Page not found" not in self.driver.page_source

            try:
                description = self.driver.find_element(
                    By.CLASS_NAME, 'viewpostbody').text
                print(description)
            except NoSuchElementException:
                description = 'N/A'

            try:
                phone_number = self.driver.find_element(
                    By.CLASS_NAME, 'userInfoContainer').text
                print(phone_number)
            except NoSuchElementException:
                phone_number = 'N/A'

            try:
                location_and_age = self.driver.find_element(
                    By.CLASS_NAME, 'viewpostlocationIconBabylon').text
                print(location_and_age)
            except NoSuchElementException:
                location_and_age = 'N/A'

            if len(self.keywords) > 0:
                if self.check_keywords(phone_number) or self.check_keywords(location_and_age) or self.check_keywords(description):
                    self.post_identifier.append(counter)
                    self.phone_number.append(phone_number)
                    self.links.append(link)
                    self.location_and_age.append(location_and_age)
                    self.description.append(description)
                    self.check_for_payment_methods(description)
                    screenshot_name = str(counter) + ".png"
                    self.capture_screenshot(screenshot_name)
                    counter += 1
                else:
                    continue
            else:
                self.post_identifier.append(counter)
                self.phone_number.append(phone_number)
                self.links.append(link)
                self.location_and_age.append(location_and_age)
                self.description.append(description)
                self.check_for_payment_methods(description)
                screenshot_name = str(counter) + ".png"
                self.capture_screenshot(screenshot_name)
                counter += 1

            if counter > 5:
                break
            #time.sleep(1)

    # TODO - move to class that handles data
    def format_data_to_csv(self):
        titled_columns = {
            'Post_identifier': self.post_identifier,
            'Phone-Number': self.phone_number,
            'Link': self.links,
            'Location/Age': self.location_and_age,
            'Description': self.description,
            'payment_methods': self.payment_methods_found
        }

        data = pd.DataFrame(titled_columns)
        data.to_csv(f'{self.scraper_directory}/escortalligator-{self.date_time}.csv', index=False, sep="\t")

    def check_for_payment_methods(self, description):
        payments = ''
        for payment in self.known_payment_methods:
            if payment in description.lower():
                print('payment method: ', payment)
                payments += payment + ' '

        if payments != '':
            self.payment_methods_found.append(payments)
        else:
            self.payment_methods_found.append('N/A')
            print('N/A')

    def capture_screenshot(self, screenshot_name):
        self.driver.save_screenshot(f'{self.screenshot_directory}/{screenshot_name}')

    # TODO - read keywords from keywords.txt
    def read_keywords(self, keywords):
        self.keywords = keywords

    def check_keywords(self, data):
        for key in self.keywords:
            if key in data:
                return True
        return False