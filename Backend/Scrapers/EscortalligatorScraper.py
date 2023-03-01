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
                                      'deposit', 'cc', 'card', 'credit card', 'applepay', 'donation', 'cash', 'visa',
                                      'paypal', 'mc', 'mastercard']

        self.date_time = None
        self.scraper_directory = None
        self.screenshot_directory = None
        self.keywords = None

        self.join_keywords = False

        self.number_of_keywords_in_post = 0
        self.keywords_found_in_post = []

        # lists to store data and then send to csv file
        self.phone_number = []
        self.description = []
        self.location_and_age = []
        self.links = []
        self.post_identifier = []
        self.payment_methods_found = []

        self.number_of_keywords_found = []
        self.keywords_found = []

        # TODO other info needs to be pulled using regex?

    def get_cities(self) -> list:
        return self.cities

    def set_city(self, city) -> None:
        self.city = city.replace(' ', '').replace('.', '')

    def set_join_keywords(self) -> None:
        self.join_keywords = True

    def initialize(self, keywords) -> None:
        # set keywords value
        self.keywords = keywords

        self.date_time = str(datetime.today())[0:19].replace(' ', '_').replace(':', '-')

        # Format website URL based on state and city
        self.get_formatted_url()

        # Selenium Web Driver setup
        options = webdriver.ChromeOptions()
        # TODO - uncomment this to run headless
        # options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)

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

    def open_webpage(self) -> None:
        self.driver.implicitly_wait(10)
        self.driver.get(self.url)
        self.driver.maximize_window()
        assert "Page not found" not in self.driver.page_source

    def close_webpage(self) -> None:
        self.driver.close()

    def get_links(self) -> list:
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

    def get_formatted_url(self) -> None:
        self.url = f'https://escortalligator.com.listcrawler.eu/brief/escorts/usa/{self.state}/{self.city}/1'
        print(f"link: {self.url}")

    def get_data(self, links) -> None:
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

            # reassign variables for each post
            self.number_of_keywords_in_post = 0
            self.keywords_found_in_post = []

            if len(self.keywords) > 0:
                if self.check_keywords(phone_number) or self.check_keywords(location_and_age) or \
                        self.check_keywords(description):

                    # check for keywords and append to lists
                    self.check_and_append_keywords(phone_number)
                    self.check_and_append_keywords(location_and_age)
                    self.check_and_append_keywords(description)

                    if self.join_keywords:
                        if len(self.keywords) == len(set(self.keywords_found_in_post)):

                            self.append_data(counter, description, link, location_and_age, phone_number)

                            screenshot_name = str(counter) + ".png"
                            self.capture_screenshot(screenshot_name)

                            # strip elements from keywords_found_in_post list using comma
                            self.keywords_found.append(', '.join(self.keywords_found_in_post))

                            # self.keywords_found.append(self.keywords_found_in_post)
                            self.number_of_keywords_found.append(self.number_of_keywords_in_post)

                            counter += 1
                        else:
                            continue
                    else:
                        self.append_data(counter, description, link, location_and_age, phone_number)
                        screenshot_name = str(counter) + ".png"
                        self.capture_screenshot(screenshot_name)

                        # strip elements from keywords_found_in_post list using comma
                        self.keywords_found.append(', '.join(self.keywords_found_in_post))

                        # self.keywords_found.append(self.keywords_found_in_post)
                        self.number_of_keywords_found.append(self.number_of_keywords_in_post)

                        counter += 1
                else:
                    continue
            else:
                self.append_data(counter, description, link, location_and_age, phone_number)

                screenshot_name = str(counter) + ".png"
                self.capture_screenshot(screenshot_name)

                # append N/A if no keywords are found
                self.keywords_found.append('N/A')
                self.number_of_keywords_found.append('N/A')

                counter += 1

                print(counter)
            print('\n')

        self.join_keywords = False

    def append_data(self, counter, description, link, location_and_age, phone_number) -> None:
        self.post_identifier.append(counter)
        self.phone_number.append(phone_number)
        self.links.append(link)
        self.location_and_age.append(location_and_age)
        self.description.append(description)
        self.check_for_payment_methods(description)

    def format_data_to_csv(self) -> None:
        titled_columns = {
            'Post-identifier': self.post_identifier,
            'Phone-Number': self.phone_number,
            'Link': self.links,
            'Location/Age': self.location_and_age,
            'Description': self.description,
            'payment-methods': self.payment_methods_found,
            'keywords-found': self.keywords_found,
            'number-of-keywords-found': self.number_of_keywords_found
        }

        data = pd.DataFrame(titled_columns)
        data.to_csv(f'{self.scraper_directory}/escortalligator-{self.date_time}.csv', index=False, sep="\t")

    def check_for_payment_methods(self, description) -> None:
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

    def capture_screenshot(self, screenshot_name) -> None:
        self.driver.save_screenshot(f'{self.screenshot_directory}/{screenshot_name}')

    def check_keywords(self, data) -> bool:
        for key in self.keywords:
            if key in data:
                return True
        return False

    def check_and_append_keywords(self, data) -> None:
        for key in self.keywords:
            if key in data.lower():
                self.keywords_found_in_post.append(key)
                print('keyword found: ', key)
                self.number_of_keywords_in_post += 1
