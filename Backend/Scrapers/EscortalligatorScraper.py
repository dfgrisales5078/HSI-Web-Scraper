from Backend.ScraperPrototype import ScraperPrototype
import time
from datetime import datetime
from selenium import webdriver
import logging
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
import pandas as pd
import os

class EscortalligatorScraper(ScraperPrototype):
    def __init__(self):
        super().__init__()
        self.driver = None
        self.location = 'fortmyers'
        self.url = f'https://escortalligator.com.listcrawler.eu/brief/escorts/usa/florida/{self.location}/1'

        self.date_time = None
        self.main_page_path = None
        self.screenshot_directory = None

        # lists to store data and then send to csv file
        self.phone_number = []
        self.description = []
        self.location_and_age = []
        self.links = []

        # TODO other info needs to be pulled using regex?

    def initialize(self):
        # set up directories to save screenshots and csv file.
        self.date_time = str(datetime.today())[0:19]
        self.date_time = self.date_time.replace(' ', '_')
        self.date_time = self.date_time.replace(':', '-')
        self.main_page_path = f'escortalligator{self.date_time}'
        os.mkdir(self.main_page_path)
        self.screenshot_directory = f'{self.main_page_path}/screenshots'
        os.mkdir(self.screenshot_directory)

        options = webdriver.FirefoxOptions()
        options.headless = False
        self.driver = webdriver.Firefox()
        self.open_webpage()
        links = self.get_links()
        self.get_data(links)
        self.close_webpage()
        self.format_data_to_csv()

    def open_webpage(self):
        self.driver.implicitly_wait(10)
        self.driver.get(self.url)
        assert "Page not found" not in self.driver.page_source

        # click on terms btn
        btn = self.driver.find_element(
            By.CLASS_NAME, 'button')
        btn.click()

        time.sleep(2)
        # click on 2nd terms btn
        btn = self.driver.find_element(
            By.CLASS_NAME, 'footer')
        btn.click()

    def close_webpage(self):
        self.driver.close()

    def get_links(self):
        posts = self.driver.find_elements(
            By.CSS_SELECTOR, '#list [href]')
        links = [post.get_attribute('href') for post in posts]
        return links[::3]

    # TODO - change if location changes?
    def get_formatted_url(self):
        pass

    def get_data(self, links):
        links = set(links)
        counter = 0
        for link in links:
            print(link)
            # append link to list
            self.links.append(link)

            self.driver.implicitly_wait(10)
            time.sleep(3)
            self.driver.get(link)
            assert "Page not found" not in self.driver.page_source

            try:
                description = self.driver.find_element(
                    By.CLASS_NAME, 'viewpostbody').text
                print(description)
                self.description.append(description)
            except NoSuchElementException:
                self.description.append('N/A')

            try:
                phone_number = self.driver.find_element(
                    By.CLASS_NAME, 'userInfoContainer').text
                print(phone_number)
                self.phone_number.append(phone_number)
            except NoSuchElementException:
                self.phone_number.append('N/A')

            try:
                location_and_age = self.driver.find_element(
                    By.CLASS_NAME, 'viewpostlocationIconBabylon').text
                print(location_and_age)
                self.location_and_age.append(location_and_age)
            except NoSuchElementException:
                self.location_and_age.append('N/A')

            screenshot_name = str(counter) + ".png"
            self.capture_screenshot(screenshot_name)
            counter += 1

            if counter > 5:
                break
            time.sleep(1)

    # TODO - move to class than handles data
    def format_data_to_csv(self):
        titled_columns = {
            'Phone-Number': self.phone_number,
            'Link': self.links,
            'Location/Age': self.location_and_age,
            'Description': self.description
        }

        data = pd.DataFrame(titled_columns)
        data.to_csv(f'{self.main_page_path}/escortalligator-{self.date_time}.csv', index=False, sep="\t")

    def capture_screenshot(self, screenshot_name):
        self.driver.save_screenshot(f'{self.screenshot_directory}/{screenshot_name}')

    # TODO - read keywords from keywords.txt
    def read_keywords(self):
        pass
