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

    def get_cities(self):
        return list(self.cities.keys())

    def set_city(self, city):
        self.city = city

    def initialize(self):
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

            self.check_for_payment_methods(description.text)

            self.post_identifier.append(counter)

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
    def read_keywords(self):
        pass
