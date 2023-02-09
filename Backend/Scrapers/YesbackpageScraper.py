import os
from datetime import datetime
import pandas as pd
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from Backend.ScraperPrototype import ScraperPrototype


class YesbackpageScraper(ScraperPrototype):

    def __init__(self):
        super().__init__()
        self.driver = None
        self.cities = {
            "florida": 'https://www.yesbackpage.com/-10/posts/8-Adult/',
            "broward": 'https://www.yesbackpage.com/70/posts/8-Adult/',
            "daytona beach": 'https://www.yesbackpage.com/71/posts/8-Adult/',
            "florida keys": 'https://www.yesbackpage.com/67/posts/8-Adult/',
            "ft myers-sw florida": 'https://www.yesbackpage.com/68/posts/8-Adult/',
            "gainesville": 'https://www.yesbackpage.com/72/posts/8-Adult/',
            "jacksonville": 'https://www.yesbackpage.com/73/posts/8-Adult/',
            "lakeland": 'https://www.yesbackpage.com/74/posts/8-Adult/',
            "miami": 'https://www.yesbackpage.com/75/posts/8-Adult/',
            "ocala": 'https://www.yesbackpage.com/76/posts/8-Adult/',
            "orlando": 'https://www.yesbackpage.com/77/posts/8-Adult/',
            "palm beach": 'https://www.yesbackpage.com/69/posts/8-Adult/',
            "panama city": 'https://www.yesbackpage.com/78/posts/8-Adult/',
            "pensacola-panhandle": 'https://www.yesbackpage.com/79/posts/8-Adult/',
            "sarasota-brandenton": 'https://www.yesbackpage.com/80/posts/8-Adult/',
            "space coast": 'https://www.yesbackpage.com/81/posts/8-Adult/',
            "st augustine": 'https://www.yesbackpage.com/82/posts/8-Adult/',
            "tallahassee": 'https://www.yesbackpage.com/83/posts/8-Adult/',
            "tampa bay area": 'https://www.yesbackpage.com/84/posts/8-Adult/',
            "treasure coast": 'https://www.yesbackpage.com/85/posts/8-Adult/',
            "west palm beach": 'https://www.yesbackpage.com/679/posts/8-Adult/'
        }
        self.city = ''
        self.url = ''
        self.known_payment_methods = ['cashapp', 'venmo', 'zelle', 'crypto', 'western union', 'no deposit',
                                      'deposit', 'cc', 'card', 'credit card', 'applepay', 'donation', 'cash']

        self.date_time = None
        self.scraper_directory = None
        self.screenshot_directory = None

        # lists to store data and then send to csv file

        # TODO services?
        self.phone_number = []
        self.link = []
        self.name = []
        self.sex = []
        self.email = []
        self.location = []
        self.description = []
        self.post_identifier = []
        self.payment_methods_found = []

        # TODO other info needs to be pulled using regex?

    def initialize(self):
        # set up directories to save screenshots and csv file.
        self.date_time = str(datetime.today())[0:19].replace(' ', '_').replace(':', '-')

        # Format website URL based on state and city
        self.get_formatted_url()

        # Selenium Web Driver setup
        options = ChromeOptions()
        options.headless = False
        self.driver = webdriver.Chrome(options=options)

        # Open Webpage with URL
        self.open_webpage()

        # Find links of posts
        links = self.get_links()

        # Create directory for search data
        self.scraper_directory = f'yesbackpage_{self.date_time}'
        os.mkdir(self.scraper_directory)

        # Create directory for search screenshots
        self.screenshot_directory = f'{self.scraper_directory}/screenshots'
        os.mkdir(self.screenshot_directory)

        self.get_data(links)
        self.format_data_to_csv()
        self.close_webpage()

    def open_webpage(self):
        self.driver.implicitly_wait(10)
        self.driver.get(self.url)
        assert "Page not found" not in self.driver.page_source

    def close_webpage(self):
        self.driver.close()

    def get_links(self):
        posts = self.driver.find_elements(
            By.CLASS_NAME, 'posttitle')
        links = [post.get_attribute('href') for post in posts]
        print(links)
        return links[2:]

    def get_formatted_url(self):
        while self.city not in self.cities.keys():
            print(list(self.cities.keys()))
            self.city = str(input("Enter city to search from above: ")).lower()
            print(f"city: {self.city}")

        self.url = self.cities.get(self.city)
        print(f"link: {self.url}")

    def get_data(self, links):
        links = set(links)

        description = ''
        counter = 0

        for link in links:
            # append link to list
            self.link.append(link)
            print(link)

            self.driver.implicitly_wait(10)
            # time.sleep(2)
            self.driver.get(link)
            assert "Page not found" not in self.driver.page_source

            try:
                name = self.driver.find_element(
                    By.XPATH, '/html/body/div[3]/div/div[1]/table/tbody/tr[1]/td/div[1]/div/table/tbody/tr[1]/td[2]')
                print(name.text[2:])
                self.name.append(name.text[2:])
            except NoSuchElementException:
                self.name.append('N/A')

            try:
                sex = self.driver.find_element(
                    By.XPATH, '/html/body/div[3]/div/div[1]/table/tbody/tr[1]/td/div[1]/div/table/tbody/tr[2]/td[2]')
                print(sex.text[2:])
                self.sex.append(sex.text[2:])
            except NoSuchElementException:
                self.sex.append('N/A')

            try:
                phone_number = self.driver.find_element(
                    By.XPATH, '/html/body/div[3]/div/div[1]/table/tbody/tr[1]/td/div[1]/div/table/tbody/tr[6]/td[2]')
                print(phone_number.text[2:])
                self.phone_number.append(phone_number.text[2:])
            except NoSuchElementException:
                self.phone_number.append('N/A')

            try:
                email = self.driver.find_element(
                    By.XPATH, '/html/body/div[3]/div/div[1]/table/tbody/tr[1]/td/div[1]/div/table/tbody/tr[8]/td[2]')
                print(email.text[2:])
                self.email.append(email.text[2:])
            except NoSuchElementException:
                self.email.append('N/A')

            try:
                location = self.driver.find_element(
                    By.XPATH, '/html/body/div[3]/div/div[1]/table/tbody/tr[1]/td/div[1]/div/table/tbody/tr[9]/td[2]')
                print(location.text[2:])
                self.location.append(location.text[2:])
            except NoSuchElementException:
                self.location.append('N/A')

            try:
                description = self.driver.find_element(
                    By.XPATH, '/html/body/div[3]/div/div[1]/table/tbody/tr[1]/td/table[2]/tbody/tr/td/div/p[2]')
                print(description.text)
                self.description.append(description.text)
            except NoSuchElementException:
                self.description.append('N/A')

            self.check_for_payment_methods(description.text)

            print("\n")

            self.post_identifier.append(counter)

            screenshot_name = str(counter) + ".png"
            self.capture_screenshot(screenshot_name)
            counter += 1

            # if counter > 10:
            #     break

    # TODO - move to class than handles data
    def format_data_to_csv(self):
        titled_columns = {
            'Post_identifier': self.post_identifier,
            'Phone Number': self.phone_number,
            'Link': self.link,
            'Location': self.location,
            'Name': self.name,
            'Sex': self.sex,
            'E-mail': self.email,
            'Description': self.description,
            'payment_methods': self.payment_methods_found
        }

        data = pd.DataFrame(titled_columns)
        data.to_csv(f'{self.scraper_directory}/yesbackpage-{self.date_time}.csv', index=False, sep="\t")

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
    def read_keywords(self):
        pass
