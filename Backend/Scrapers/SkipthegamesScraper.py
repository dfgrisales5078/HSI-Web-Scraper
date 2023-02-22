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
        self.cities = {
            "bonita springs": 'https://skipthegames.com/posts/bonita-springs-fl',
            "bradenton": 'https://skipthegames.com/posts/bradenton',
            "cape coral": 'https://skipthegames.com/posts/cape-coral-fl',
            "fort myers": 'https://skipthegames.com/posts/fort-myers',
            "ocala": 'https://skipthegames.com/posts/ocala',
            "okaloosa": 'https://skipthegames.com/posts/okaloosa',
            "orlando": 'https://skipthegames.com/posts/orlando',
            "palm bay": 'https://skipthegames.com/posts/palmbay',
            "gainesville": 'https://skipthegames.com/posts/gainesville',
            "jacksonville": 'https://skipthegames.com/posts/jacksonville',
            "keys": 'https://skipthegames.com/posts/keys',
            "miami": 'https://skipthegames.com/posts/miami',
            "naples": 'https://skipthegames.com/posts/naples-fl',
            "st. augustine": 'https://skipthegames.com/posts/st-augustine',
            "tallahassee": 'https://skipthegames.com/posts/tallahassee',
            "tampa": 'https://skipthegames.com/posts/tampa',
            "sarasota": 'https://skipthegames.com/posts/sarasota',
            "space coast": 'https://skipthegames.com/posts/space-coast',
            "venice": 'https://skipthegames.com/posts/venice-fl',
            "west palm beach": 'https://skipthegames.com/posts/west-palm-beach'
        }
        self.city = ''
        self.url = ''

        self.known_payment_methods = ['cashapp', 'venmo', 'zelle', 'crypto', 'western union', 'no deposit',
                                      'deposit', 'cc', 'credit card', 'card', 'applepay', 'donation', 'cash']

        self.date_time = None
        self.main_page_path = None
        self.screenshot_directory = None
        self.keywords = None

        self.number_of_keywords_in_post = 0
        self.keywords_found_in_post = []

        # lists to store data and then send to csv file
        self.link = []
        self.about_info = []
        self.description = []
        self.services = []
        self.post_identifier = []
        self.payment_methods_found = []

        self.number_of_keywords_found = []
        self.keywords_found = []

        # TODO these need to be pulled from about_info, description, or activities using regex?
        # self.phone_number = []
        # self.name = []
        # self.sex = []
        # self.email = []
        # self.payment_method = []
        # self.location = []

    def get_cities(self) -> list:
        return list(self.cities.keys())

    def set_city(self, city) -> None:
        self.city = city

    def initialize(self, keywords) -> None:
        # set keywords value
        self.keywords = keywords

        # set up directories to save screenshots and csv file.
        self.date_time = str(datetime.today())[0:19].replace(' ', '_').replace(':', '-')

        # Format website URL based on state and city
        self.get_formatted_url()

        # Selenium Web Driver setup
        options = uc.ChromeOptions()
        options.headless = False
        self.driver = uc.Chrome(use_subprocess=True, options=options)

        # Open Webpage with URL
        self.open_webpage()

        # Find links of posts
        links = self.get_links()

        # create directories for screenshot and csv
        self.main_page_path = f'skipthegames_{self.date_time}'
        os.mkdir(self.main_page_path)
        self.screenshot_directory = f'{self.main_page_path}/screenshots'
        os.mkdir(self.screenshot_directory)

        self.get_data(links)
        self.format_data_to_csv()
        self.close_webpage()

    def open_webpage(self) -> None:
        self.driver.implicitly_wait(10)
        self.driver.get(self.url)
        assert "Page not found" not in self.driver.page_source

    def close_webpage(self) -> None:
        self.driver.close()

    def get_links(self) -> set:
        posts = self.driver.find_elements(
            By.CSS_SELECTOR, 'html.no-js body div table.two-col-wrap tbody tr '
                             'td#gallery_view.listings-with-sidebar.list-search-results.gallery div.full-width '
                             'div.small-16.columns div.clsfds-display-mode.gallery div.day-gallery [href]')
        links = [post.get_attribute('href') for post in posts]

        # remove sponsored links
        links = [link for link in links if link.startswith('https://skipthegames.com/posts/')]

        print([link for link in set(links)])
        print('# of links:', len(set(links)))
        return set(links)

    # TODO - change if location changes?
    def get_formatted_url(self) -> None:
        self.url = self.cities.get(self.city)
        print(f"link: {self.url}")

    def get_data(self, links) -> None:
        counter = 0

        for link in links:
            print(link)

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

            # reassign variables for each post
            self.number_of_keywords_in_post = 0
            self.keywords_found_in_post = []

            if len(self.keywords) > 0:
                if self.check_keywords(about_info) or self.check_keywords(services) or self.check_keywords(description):

                    self.check_and_append_keywords(about_info)
                    self.check_and_append_keywords(services)
                    self.check_and_append_keywords(description)

                    self.post_identifier.append(counter)
                    self.link.append(link)
                    self.about_info.append(about_info)
                    self.services.append(services)
                    self.description.append(description)
                    self.check_for_payment_methods(description)
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
                self.post_identifier.append(counter)
                self.link.append(link)
                self.about_info.append(about_info)
                self.services.append(services)
                self.description.append(description)
                self.check_for_payment_methods(description)
                screenshot_name = str(counter) + ".png"
                self.capture_screenshot(screenshot_name)

                # append N/A if no keywords are found
                self.keywords_found.append('N/A')
                self.number_of_keywords_found.append('N/A')

                counter += 1
            print('\n')

    def format_data_to_csv(self) -> None:
        titled_columns = {
            'Post-identifier': self.post_identifier,
            'Link': self.link,
            'about-info': self.about_info,
            'services': self.services,
            'Description': self.description,
            'payment-methods': self.payment_methods_found,
            'keywords-found': self.keywords_found,
            'number-of-keywords-found': self.number_of_keywords_found
        }

        data = pd.DataFrame(titled_columns)
        data.to_csv(f'{self.main_page_path}/skipthegames-{self.date_time}.csv', index=False, sep="\t")

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
