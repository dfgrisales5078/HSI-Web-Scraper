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
                                      'deposit', 'cc', 'card', 'credit card', 'applepay', 'donation', 'cash', 'visa',
                                      'paypal', 'mc', 'mastercard']

        self.date_time = None
        self.scraper_directory = None
        self.screenshot_directory = None
        self.keywords = None

        self.join_keywords = False

        self.number_of_keywords_in_post = 0
        self.keywords_found_in_post = []
        self.only_posts_with_payment_methods = False

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

    def set_join_keywords(self) -> None:
        self.join_keywords = True

    def set_only_posts_with_payment_methods(self) -> None:
        self.only_posts_with_payment_methods = True

    def initialize(self, keywords) -> None:
        # set keywords value
        self.keywords = keywords

        # Date and time of search
        self.date_time = str(datetime.today())[0:19].replace(' ', '_').replace(':', '-')

        # Format website URL based on state and city
        self.get_formatted_url()

        # Selenium Web Driver setup
        options = uc.ChromeOptions()
        # TODO - uncomment to run headless
        # options.add_argument('--headless')
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
        self.format_data_to_csv()
        self.close_webpage()
        self.reset_variables()


    def open_webpage(self) -> None:
        self.driver.implicitly_wait(10)
        self.driver.get(self.url)
        self.driver.maximize_window()
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

            if self.join_keywords and self.only_posts_with_payment_methods:
                print("if l187")
                if self.check_keywords(profile_header) or self.check_keywords(description) \
                        or self.check_keywords(info_details) or self.check_keywords(contact_details):
                    counter = self.join_with_payment_methods(contact_details, counter, description, info_details, link, profile_header)

            elif self.join_keywords or self.only_posts_with_payment_methods:
                print(' line 193')
                if self.join_keywords:
                    print('line 195')
                    if self.check_keywords(profile_header) or self.check_keywords(description) \
                            or self.check_keywords(info_details) or self.check_keywords(contact_details):
                        self.check_keywords_found(contact_details, description, info_details, profile_header)
                        counter = self.join_inclusive(contact_details, counter, description, info_details, link, profile_header)

                elif self.only_posts_with_payment_methods:
                    print('line 202')
                    if len(self.keywords) > 0:
                        print('line 204')
                        if self.check_keywords(profile_header) or self.check_keywords(description) \
                                or self.check_keywords(info_details) or self.check_keywords(contact_details):
                            self.check_keywords_found(contact_details, description, info_details, profile_header)

                    else:
                        print('210')
                    counter = self.payment_methods_only(contact_details, counter, description, info_details, link, profile_header)

            else:
                print('214')
                if len(self.keywords) > 0:
                    print('line 216')
                    if self.check_keywords(profile_header) or self.check_keywords(description) \
                            or self.check_keywords(info_details) or self.check_keywords(contact_details):
                        self.check_keywords_found(contact_details, description, info_details, profile_header)
                        self.append_data(contact_details, counter, description, info_details, link, profile_header)
                        screenshot_name = str(counter) + ".png"
                        self.capture_screenshot(screenshot_name)
                        counter += 1

                else:
                    print('225')
                    self.append_data(contact_details, counter, description, info_details, link, profile_header)
                    screenshot_name = str(counter) + ".png"
                    self.capture_screenshot(screenshot_name)
                    counter += 1
            print('\n')

        self.join_keywords = False

    def join_with_payment_methods(self, contact_details, counter, description, info_details, link, profile_header):
        if self.check_for_payment_methods(description) and len(self.keywords) == len(set(self.keywords_found_in_post)):
            self.append_data(contact_details, counter, description, info_details, link, profile_header)
            screenshot_name = str(counter) + ".png"
            self.capture_screenshot(screenshot_name)

            return counter + 1
        return counter

    def check_keywords_found(self, contact_details, description, info_details, profile_header):
        self.check_and_append_keywords(contact_details)
        self.check_and_append_keywords(description)
        self.check_and_append_keywords(info_details)
        self.check_and_append_keywords(profile_header)

    def reset_variables(self):
        self.post_identifier = []
        self.link = []
        self.profile_header = []
        self.about_info = []
        self.info_details = []
        self.contact_details = []
        self.payment_methods_found = []
        self.keywords_found = []
        self.number_of_keywords_found = []
        self.only_posts_with_payment_methods = False
        self.join_keywords = False

    def append_data(self, contact_details, counter, description, info_details, link, profile_header) -> None:
        print('Append the dam data --->>>>')

        self.post_identifier.append(counter)
        self.link.append(link)
        self.profile_header.append(profile_header)
        self.about_info.append(description)
        self.info_details.append(info_details)
        self.contact_details.append(contact_details)
        self.check_and_append_payment_methods(description)
        self.keywords_found.append(', '.join(self.keywords_found_in_post) or 'N/A')
        self.number_of_keywords_found.append(self.number_of_keywords_in_post or 'N/A')


    def format_data_to_csv(self) -> None:
        print(len(self.post_identifier))
        print(len(self.profile_header))
        print(len(self.about_info))
        print(len(self.info_details))
        print(len(self.contact_details))
        print(len(self.payment_methods_found))
        print(len(self.keywords_found))
        print(len(self.number_of_keywords_found))

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

    def check_for_payment_methods(self, description) -> bool:
        for payment in self.known_payment_methods:
            if payment in description.lower():
                print('payment method: ', payment)
                return True
        return False

    def check_and_append_payment_methods(self, description):
        payments = ''
        for payment in self.known_payment_methods:
            if payment in description.lower():
                print('payment method: ', payment)
                payments += payment + '\n'

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

    def join_inclusive(self, contact_details, counter, description, info_details, link, profile_header):
        if len(self.keywords) == len(set(self.keywords_found_in_post)):
            self.append_data(contact_details, counter, description, info_details, link, profile_header)

            screenshot_name = str(counter) + ".png"
            self.capture_screenshot(screenshot_name)

            return counter + 1
        return counter

    def payment_methods_only(self, about_info, counter, description, link, services, profile_header) -> int:
        if self.check_for_payment_methods(description):
            print('l382 if')
            self.append_data(about_info, counter, description, link, services, profile_header)
            screenshot_name = str(counter) + ".png"
            self.capture_screenshot(screenshot_name)

            return counter + 1
        return counter
