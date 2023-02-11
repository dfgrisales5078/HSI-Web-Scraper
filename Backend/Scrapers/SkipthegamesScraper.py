import os
from datetime import datetime
import pandas as pd
import undetected_chromedriver as uc
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from Backend.ScraperPrototype import ScraperPrototype


class SkipthegamesScraper(ScraperPrototype):
    def __init__(self):
        super().__init__()
        self.driver = None
        self.location = 'fort-myers'
        self.url = f'https://www.skipthegames.com/posts/{self.location}/'

        self.known_payment_methods = ['cashapp', 'venmo', 'zelle', 'crypto', 'western union', 'no deposit',
                                      'deposit', 'cc', 'credit card', 'card', 'applepay', 'donation', 'cash']

        self.date_time = None
        self.main_page_path = None
        self.screenshot_directory = None
        self.keywords = None

        # lists to store data and then send to csv file
        self.link = []
        self.about_info = []
        self.description = []
        self.services = []
        self.post_identifier = []
        self.payment_methods_found = []

        # TODO these need to be pulled from about_info, description, or activities using regex?
        # self.phone_number = []
        # self.name = []
        # self.sex = []
        # self.email = []
        # self.payment_method = []
        # self.location = []

    def initialize(self, keywords):
        self.read_keywords(keywords)
        # set up directories to save screenshots and csv file.
        self.date_time = str(datetime.today())[0:19]
        self.date_time = self.date_time.replace(' ', '_').replace(':', '-')
        self.main_page_path = f'skipthegames_{self.date_time}'
        os.mkdir(self.main_page_path)
        self.screenshot_directory = f'{self.main_page_path}/screenshots'
        os.mkdir(self.screenshot_directory)

        options = uc.ChromeOptions()
        options.headless = True
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
            print(link)

            # self.driver.implicitly_wait(2)
            # time.sleep(1)
            self.driver.get(link)
            assert "Page not found" not in self.driver.page_source

            try:
                about_info = self.driver.find_element(
                    By.XPATH, '/html/body/div[7]/div/div[2]/div/table/tbody').text
                print(about_info)
            except NoSuchElementException:
                about_info = 'N/A'

            try:
                services = self.driver.find_element(
                    By.XPATH, '//*[@id="post-services"]').text
                print(services)
            except NoSuchElementException:
                services = 'N/A'

            try:
                description = self.driver.find_element(
                    By.XPATH, '/html/body/div[7]/div/div[2]/div/div[1]/div').text
                print(description)
            except NoSuchElementException:
                description = 'N/A'

            if len(self.keywords) > 0:
                if self.check_keywords(about_info) or self.check_keywords(services) or self.check_keywords(description):
                    self.post_identifier.append(counter)
                    self.link.append(link)
                    self.about_info.append(about_info)
                    self.services.append(services)
                    self.description.append(description)
                    self.check_for_payment_methods(description)
                    screenshot_name = str(counter) + ".png"
                    self.capture_screenshot(screenshot_name)
                    counter += 1
                else:
                    continue
            else:
                self.post_identifier.append(counter)
                self.link.append(link)
                self.about_info.append(about_info)
                self.services.append(services)
                self.description.append(description)
                self.check_for_payment_methods(description)
                screenshot_name = str(counter) + ".png"
                self.capture_screenshot(screenshot_name)
                counter += 1

            if counter > 5:
                break

    # TODO - move to class than handles data
    def format_data_to_csv(self):
        titled_columns = {
            'Post_identifier': self.post_identifier,
            'Link': self.link,
            'about-info': self.about_info,
            'services': self.services,
            'Description': self.description,
            'payment_methods': self.payment_methods_found
        }

        data = pd.DataFrame(titled_columns)
        data.to_csv(f'{self.main_page_path}/skipthegames-{self.date_time}.csv', index=False, sep="\t")

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
