from Backend.ScraperPrototype import ScraperPrototype
import time
from datetime import datetime
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options as ChromeOptions
import logging
from selenium.webdriver.common.by import By
import pandas as pd
import undetected_chromedriver as uc


class SkipthegamesScraper(ScraperPrototype):
    def __init__(self):
        super().__init__()
        self.driver = None
        self.location = 'fort-myers'
        self.url = f'https://www.skipthegames.com/posts/{self.location}/'

        # lists to store data and then send to csv file
        self.link = []
        self.about_info = []
        self.description = []
        self.services = []

        # TODO these need to be pulled from about_info, description, or activities using regex?
        # self.phone_number = []
        # self.name = []
        # self.sex = []
        # self.email = []
        # self.payment_method = []
        # self.location = []

    def initialize(self):
        options = uc.ChromeOptions()
        options.headless = False
        self.driver = uc.Chrome(use_subprocess=True, options=options)
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

    # TODO fix bug to get the correct links
    def get_links(self):
        posts = self.driver.find_elements(
            By.CSS_SELECTOR, 'html.no-js body div table.two-col-wrap tbody tr '
                             'td#gallery_view.listings-with-sidebar.list-search-results.gallery div.full-width '
                             'div.small-16.columns div.clsfds-display-mode.gallery div.day-gallery [href]')
        links = [post.get_attribute('href') for post in posts]

        print([link for link in set(links)])
        print('# of links:', len(set(links)))
        return links

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

            # self.driver.implicitly_wait(2)
            # time.sleep(1)
            self.driver.get(link)
            assert "Page not found" not in self.driver.page_source

            try:
                about_info = self.driver.find_element(
                    By.XPATH, '/html/body/div[7]/div/div[2]/div/table/tbody')
                print(about_info.text)
                self.about_info.append(about_info.text)
            except NoSuchElementException:
                self.about_info.append('N/A')

            try:
                services = self.driver.find_element(
                    By.XPATH, '//*[@id="post-services"]')
                print(services.text)
                self.services.append(services.text)
            except NoSuchElementException:
                self.services.append('N/A')

            try:
                description = self.driver.find_element(
                    By.XPATH, '/html/body/div[7]/div/div[2]/div/div[1]/div')
                print(description.text)
                self.description.append(description.text)
            except NoSuchElementException:
                self.description.append('N/A')

            screenshot_name = str(counter) + ".png"
            self.capture_screenshot(screenshot_name)
            counter += 1

            if counter > 5:
                break

    # TODO - move to class than handles data
    def format_data_to_csv(self):
        titled_columns = {
            'Link': self.link,
            'about-info': self.about_info,
            'services': self.services,
            'Description': self.description
        }

        data = pd.DataFrame(titled_columns)
        data.to_csv(f'skipthegames-{str(datetime.today())[0:10]}.csv', index=False, sep="\t")

    def capture_screenshot(self, screenshot_name):
        self.driver.save_screenshot(f'screenshots/{screenshot_name}')

    # TODO - read keywords from keywords.txt
    def read_keywords(self):
        pass
