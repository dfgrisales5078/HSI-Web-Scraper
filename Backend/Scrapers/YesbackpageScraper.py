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
        self.url = f'https://www.yesbackpage.com/68/posts/8-Adult/122-Female-Escorts'

        self.date_time = None
        self.main_page_path = None
        self.screenshot_directory = None

        # lists to store data and then send to csv file
        self.phone_number = []
        self.link = []
        self.name = []
        self.sex = []
        self.email = []
        self.location = []
        self.description = []
        self.post_identifier = []

        # TODO other info needs to be pulled using regex?

    def initialize(self):
        # set up directories to save screenshots and csv file.
        self.date_time = str(datetime.today())[0:19]
        self.date_time = self.date_time.replace(' ', '_')
        self.date_time = self.date_time.replace(':', '-')
        self.main_page_path = f'yesbackpage_{self.date_time}'
        os.mkdir(self.main_page_path)
        self.screenshot_directory = f'{self.main_page_path}/screenshots'
        os.mkdir(self.screenshot_directory)

        options = ChromeOptions()
        options.headless = False
        self.driver = webdriver.Chrome(options=options)
        self.open_webpage()

        links = self.get_links()
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
            By.CSS_SELECTOR, '#mainCellWrapper > div.mainBody > table [href]')
        links = [post.get_attribute('href') for post in posts]
        return links[2:]

    # TODO - change if location changes?
    def get_formatted_url(self):
        pass

    def get_data(self, links):
        links = set(links)
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

            print("\n")

            self.post_identifier.append(counter)

            screenshot_name = str(counter) + ".png"
            self.capture_screenshot(screenshot_name)
            counter += 1

            if counter > 5:
                break

    # TODO - move to class than handles data
    def format_data_to_csv(self):
        titled_columns = {
            'Phone Number': self.phone_number,
            'Link': self.link,
            'Location': self.location,
            'Name': self.name,
            'Sex': self.sex,
            'E-mail': self.email,
            'Description': self.description,
            'Post_identifier': self.post_identifier
        }

        data = pd.DataFrame(titled_columns)
        data.to_csv(f'{self.main_page_path}/yesbackpage-{self.date_time}.csv', index=False, sep="\t")

    def capture_screenshot(self, screenshot_name):
        self.driver.save_screenshot(f'{self.screenshot_directory}/{screenshot_name}')

    # TODO - read keywords from keywords.txt
    def read_keywords(self):
        pass
