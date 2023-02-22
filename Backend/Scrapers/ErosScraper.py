from Backend.ScraperPrototype import ScraperPrototype
import time
from datetime import datetime
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
import pandas as pd
import undetected_chromedriver as uc
import os


class ErosScraper(ScraperPrototype):
    def __init__(self):
        super().__init__()
        self.driver = None

        self.cities = {
            "miami": 'https://www.eros.com/florida/miami/sections/miami_escorts.htm',
            "naples": 'https://www.eros.com/florida/naples/sections/naples_escorts.htm',
            "north florida": 'https://www.eros.com/florida/north_florida/sections/north_florida_escorts.htm',
            "orlando": 'https://www.eros.com/florida/tampa/sections/tampa_escorts.htm',
            "tampa": 'https://www.eros.com/florida/tampa/sections/tampa_escorts.htm'
        }
        self.city = ''
        self.url = ''
        self.known_payment_methods = ['cashapp', 'venmo', 'zelle', 'crypto', 'western union', 'no deposit',
                                      'deposit', 'cc', 'credit card', 'card', 'applepay', 'donation', 'cash']

        self.date_time = None
        self.scraper_directory = None
        self.screenshot_directory = None
        self.keywords = None

        self.number_of_keywords_in_post = 0
        self.keywords_found_in_post = []

        # lists to store data and then send to csv file
        self.post_identifier = []
        self.link = []
        self.profile_header = []
        self.about_info = []
        self.info_details = []
        self.contact_details = []
        self.payment_methods_found = []

        self.number_of_keywords_found = []
        self.keywords_found = []

        # TODO other info needs to be pulled using regex?
    def get_cities(self) -> list:
        return list(self.cities.keys())

    def set_city(self, city) -> None:
        self.city = city

    def initialize(self, keywords) -> None:
        # set keywords value
        self.keywords = keywords

        # Date and time of search
        self.date_time = str(datetime.today())[0:19].replace(' ', '_').replace(':', '-')

        # Format website URL based on state and city
        self.get_formatted_url()

        # Selenium Web Driver setup
        options = uc.ChromeOptions()
        options.headless = False
        self.driver = uc.Chrome(use_subprocess=True, options=options)

        # Open Webpage with URL
        self.open_webpage()
        time.sleep(10)

        # Find links of posts
        links = self.get_links()

        # Create directory for search data
        self.scraper_directory = f'eros_{self.date_time}'
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
        assert "Page not found" not in self.driver.page_source
        # self.driver.maximize_window()

    def close_webpage(self) -> None:
        self.driver.close()

    def get_links(self) -> set:
        try:
            # Find website agreement
            self.driver.find_element(
                By.XPATH, '//*[@id="agree_enter_website"]').click()
            self.driver.find_element(
                By.XPATH, '// *[ @ id = "ageModal"] / div / div / div[2] / button').click()
        except NoSuchElementException:
            print("There was a problem with finding the website.")
            exit(1)

        try:
            # Find all profile links
            posts = self.driver.find_elements(
                By.CSS_SELECTOR, '#listing > div.grid.fourPerRow.mobile.switchable [href]')
        except NoSuchElementException:
            print("There was a problem finding posts.")
            exit(1)

        if posts:
            links = [post.get_attribute('href') for post in posts]
            print(set(links))
        else:
            print("No posts found.")
            exit(1)

        return set(links)

    def get_formatted_url(self) -> None:
        self.url = self.cities.get(self.city)
        print(f"link: {self.url}")

    def get_data(self, links) -> None:
        description = ''
        counter = 0

        for link in links:
            print(link)

            self.driver.implicitly_wait(10)
            self.driver.get(link)
            assert "Page not found" not in self.driver.page_source

            try:
                profile_header = self.driver.find_element(
                    By.XPATH, '//*[@id="pageone"]/div[1]').text
                print(profile_header)
            except NoSuchElementException:
                profile_header = 'N/A'

            try:
                description = self.driver.find_element(
                    By.XPATH, '// *[ @ id = "pageone"] / div[3] / div / div[1] / div[2]').text
                print(description)
            except NoSuchElementException:
                description = 'N/A'

            try:
                info_details = self.driver.find_element(
                    By.XPATH, '//*[@id="pageone"]/div[3]/div/div[2]/div[1]/div').text
                print(info_details)
            except NoSuchElementException:
                info_details = 'N/A'

            try:
                contact_details = self.driver.find_element(
                    By.XPATH, '//*[@id="pageone"]/div[3]/div/div[2]/div[2]').text
                print(contact_details)
            except NoSuchElementException:
                contact_details = 'N/A'

            # reassign variables for each post
            self.number_of_keywords_in_post = 0
            self.keywords_found_in_post = []

            if len(self.keywords) > 0:
                if self.check_keywords(profile_header) or self.check_keywords(description) \
                        or self.check_keywords(info_details) or self.check_keywords(contact_details):

                    # check for keywords and append to lists
                    self.check_and_append_keywords(profile_header)
                    self.check_and_append_keywords(description)
                    self.check_and_append_keywords(info_details)
                    self.check_and_append_keywords(contact_details)

                    self.post_identifier.append(counter)
                    self.link.append(link)
                    self.profile_header.append(profile_header)
                    self.about_info.append(description)
                    self.info_details.append(info_details)
                    self.contact_details.append(contact_details)
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
                self.profile_header.append(profile_header)
                self.about_info.append(description)
                self.info_details.append(info_details)
                self.contact_details.append(contact_details)
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
            'link': self.link,
            'profile-header': self.profile_header,
            'about-info': self.about_info,
            'info-details': self.info_details,
            'contact-details': self.contact_details,
            'payment-methods': self.payment_methods_found,
            'keywords-found': self.keywords_found,
            'number-of-keywords-found': self.number_of_keywords_found
        }

        data = pd.DataFrame(titled_columns)
        data.to_csv(f'{self.scraper_directory}/eros-{self.date_time}.csv', index=False, sep='\t')

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
        print(f'{self.screenshot_directory}/{screenshot_name}')
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
