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

        # lists to store data and then send to csv file
        self.post_identifier = []
        self.link = []
        self.profile_header = []
        self.about_info = []
        self.info_details = []
        self.contact_details = []
        self.payment_methods_found = []

        # TODO other info needs to be pulled using regex?

    def initialize(self):
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
        self.driver.maximize_window()

    def close_webpage(self) -> None:
        self.driver.close()

    def get_links(self):
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

    def get_formatted_url(self):
        while self.city not in self.cities.keys():
            print(list(self.cities.keys()))
            self.city = str(input("Enter city to search from above: ")).lower()
            print(f"city: {self.city}")

        self.url = self.cities.get(self.city)
        print(f"link: {self.url}")

    def get_data(self, links):
        description = ''
        counter = 0

        for link in links:
            # append link to list
            self.link.append(link)
            print(link)

            self.driver.implicitly_wait(10)
            self.driver.get(link)
            assert "Page not found" not in self.driver.page_source

            try:
                profile_header = self.driver.find_element(
                    By.XPATH, '//*[@id="pageone"]/div[1]')
                print(profile_header.text)
                self.profile_header.append(profile_header.text)
            except NoSuchElementException:
                self.profile_header.append('N/A')

            try:
                description = self.driver.find_element(
                    By.XPATH, '// *[ @ id = "pageone"] / div[3] / div / div[1] / div[2]').text
                print(description)
                self.about_info.append(description)
            except NoSuchElementException:
                self.about_info.append('N/A')

            self.check_for_payment_methods(description)

            try:
                info_details = self.driver.find_element(
                    By.XPATH, '//*[@id="pageone"]/div[3]/div/div[2]/div[1]/div')
                print(info_details.text)
                self.info_details.append(info_details.text)
            except NoSuchElementException:
                self.info_details.append('N/A')

            try:
                contact_details = self.driver.find_element(
                    By.XPATH, '//*[@id="pageone"]/div[3]/div/div[2]/div[2]')
                print(contact_details.text)
                self.contact_details.append(contact_details.text)
            except NoSuchElementException:
                print('N/A')
                self.contact_details.append('N/A')

            # Append post count as unique identifier
            self.post_identifier.append(counter)
            # Capture screenshot with unique identifier
            screenshot_name = str(counter) + ".png"
            self.capture_screenshot(screenshot_name)
            counter += 1

            if counter > 3:
                break

    # TODO - move to class than handles data
    def format_data_to_csv(self):
        titled_columns = {
            'Post_identifier': self.post_identifier,
            'link': self.link,
            'profile_header': self.profile_header,
            'about_info': self.about_info,
            'info_details': self.info_details,
            'contact_details': self.contact_details,
            'payment_methods': self.payment_methods_found
        }

        data = pd.DataFrame(titled_columns)
        data.to_csv(f'{self.scraper_directory}/eros-{self.date_time}.csv', index=False, sep='\t')

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
        print(f'{self.screenshot_directory}/{screenshot_name}')
        self.driver.save_screenshot(f'{self.screenshot_directory}/{screenshot_name}')

    # TODO - read keywords from keywords.txt
    def read_keywords(self) -> str:
        return ' '.join(self.keywords)
