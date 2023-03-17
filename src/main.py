import json
import qdarkstyle as qdarkstyle
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QWidget, QTabWidget
from abc import ABC, abstractmethod
import time
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
import pandas as pd
import undetected_chromedriver as uc
import os
from datetime import datetime
from PyQt6 import QtCore, QtGui, QtWidgets

# ---------------------------- Code to Show Icon on Windows Taskbar ----------------------------

basedir = os.path.dirname(__file__)
try:
    from ctypes import windll

    myappid = 'hsi.scraper.version1.0'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except:
    pass


# ---------------------------- ScraperPrototype ----------------------------
class ScraperPrototype(ABC):
    def __init__(self):
        self.location = None
        self.keywords = Keywords()
        self.join = None
        self.payment = None
        self.url = None
        self.text_search = None

    @abstractmethod
    def initialize(self, keywords):
        pass

    @abstractmethod
    def open_webpage(self):
        pass

    @abstractmethod
    def close_webpage(self):
        pass

    @abstractmethod
    def get_formatted_url(self):
        pass

    @abstractmethod
    def get_data(self, links):
        pass

    @abstractmethod
    def check_for_payment_methods(self, description):
        pass

    @abstractmethod
    def capture_screenshot(self, screenshot_name):
        pass

    @abstractmethod
    def check_keywords(self, text):
        pass

    @abstractmethod
    def check_and_append_keywords(self, text):
        pass


# ---------------------------- YesBackPage ----------------------------
class YesbackpageScraper(ScraperPrototype):

    def __init__(self):
        super().__init__()
        self.path = None
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
                                      'deposit', 'cc', 'card', 'credit card', 'applepay', 'donation', 'cash', 'visa',
                                      'paypal', 'mc', 'mastercard']

        self.date_time = None
        self.scraper_directory = None
        self.screenshot_directory = None
        self.keywords = None

        self.join_keywords = False
        self.number_of_keywords_in_post = 0
        self.keywords_found_in_post = []

        # lists to store data and then send to csv file

        self.phone_number = []
        self.link = []
        self.name = []
        self.sex = []
        self.email = []
        self.location = []
        self.description = []
        self.post_identifier = []
        self.payment_methods_found = []
        self.services = []

        self.number_of_keywords_found = []
        self.keywords_found = []

    def get_cities(self) -> list:
        return list(self.cities.keys())

    def set_city(self, city) -> None:
        self.city = city

    def set_join_keywords(self) -> None:
        self.join_keywords = True

    def set_path(self, path) -> None:
        self.path = path

    def initialize(self, keywords) -> None:
        # set keywords value
        self.keywords = keywords

        # set up directories to save screenshots and csv file.
        self.date_time = str(datetime.today())[0:19].replace(' ', '_').replace(':', '-')

        # Format website URL based on state and city
        self.get_formatted_url()

        options = uc.ChromeOptions()
        # TODO - uncomment this line to run headless
        options.add_argument('--headless')
        self.driver = uc.Chrome(subprocress=True, options=options)

        # Open Webpage with URL
        self.open_webpage()

        # Find links of posts
        links = self.get_links()

        # Create directory for search data
        self.scraper_directory = f'{self.path}/yesbackpage_{self.date_time}'
        os.mkdir(self.scraper_directory)

        # Create directory for search screenshots
        self.screenshot_directory = f'{self.scraper_directory}/screenshots'
        os.mkdir(self.screenshot_directory)

        self.get_data(links)
        self.format_data_to_csv()
        self.close_webpage()
        self.reset_variables()

    def open_webpage(self) -> None:
        self.driver.implicitly_wait(10)
        self.driver.get(self.url)
        self.driver.maximize_window()
        assert "Page not found" not in self.driver.page_source

    def close_webpage(self) -> None:
        self.driver.close()

    def get_links(self) -> list:
        posts = self.driver.find_elements(
            By.CLASS_NAME, 'posttitle')
        links = [post.get_attribute('href') for post in posts]
        return links[2:]

    def get_formatted_url(self) -> None:
        self.url = self.cities.get(self.city)

    def get_data(self, links) -> None:
        links = links

        counter = 0

        for link in links:
            self.driver.implicitly_wait(10)
            self.driver.get(link)
            assert "Page not found" not in self.driver.page_source

            try:
                description = self.driver.find_element(
                    By.XPATH, '/html/body/div[3]/div/div[1]/table/tbody/tr[1]/td/table[2]/tbody/'
                              'tr/td/div/p[2]').text
            except NoSuchElementException:
                description = 'N/A'

            try:
                name = self.driver.find_element(
                    By.XPATH, '/html/body/div[3]/div/div[1]/table/tbody/tr[1]/td/div[1]/div/table/'
                              'tbody/tr[1]/td[2]').text[2:]
            except NoSuchElementException:
                name = 'N/A'

            try:
                sex = self.driver.find_element(
                    By.XPATH, '/html/body/div[3]/div/div[1]/table/tbody/tr[1]/td/div[1]/div/table/'
                              'tbody/tr[2]/td[2]').text[2:]
            except NoSuchElementException:
                sex = 'N/A'

            try:
                phone_number = self.driver.find_element(
                    By.XPATH, '/html/body/div[3]/div/div[1]/table/tbody/tr[1]/td/div[1]/div/table/'
                              'tbody/tr[6]/td[2]').text[2:]
            except NoSuchElementException:
                phone_number = 'NA'

            try:
                email = self.driver.find_element(
                    By.XPATH, '/html/body/div[3]/div/div[1]/table/tbody/tr[1]/td/div[1]/div/table/'
                              'tbody/tr[8]/td[2]').text[2:]
            except NoSuchElementException:
                email = 'N/A'

            try:
                location = self.driver.find_element(
                    By.XPATH, '/html/body/div[3]/div/div[1]/table/tbody/tr[1]/td/div[1]/div/table/'
                              'tbody/tr[9]/td[2]').text[2:]
            except NoSuchElementException:
                location = 'N/A'

            try:
                services = self.driver.find_element(
                    By.XPATH, '//*[@id="mainCellWrapper"]/div/table/tbody/tr/td/div[1]/div/table/'
                              'tbody/tr[5]/td[2]').text[2:]
            except NoSuchElementException:
                services = 'N/A'

            # reassign variables for each post
            self.number_of_keywords_in_post = 0
            self.keywords_found_in_post = []

            if len(self.keywords) > 0:
                if self.check_keywords(description) or self.check_keywords(name) or self.check_keywords(sex) \
                        or self.check_keywords(phone_number) or self.check_keywords(email) \
                        or self.check_keywords(location) or self.check_keywords(services):

                    # check for keywords and append to lists
                    self.check_and_append_keywords(description)
                    self.check_and_append_keywords(name)
                    self.check_and_append_keywords(sex)
                    self.check_and_append_keywords(phone_number)
                    self.check_and_append_keywords(email)
                    self.check_and_append_keywords(location)
                    self.check_and_append_keywords(services)

                    if self.join_keywords:
                        if len(self.keywords) == len(set(self.keywords_found_in_post)):
                            self.append_data(counter, description, email, link, location, name, phone_number, services,
                                             sex)
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
                        self.append_data(counter, description, email, link, location, name, phone_number, services,
                                         sex)
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
                self.append_data(counter, description, email, link, location, name, phone_number, services,
                                 sex)
                screenshot_name = str(counter) + ".png"
                self.capture_screenshot(screenshot_name)

                # append N/A if no keywords are found
                self.keywords_found.append('N/A')
                self.number_of_keywords_found.append('N/A')

                counter += 1

        self.join_keywords = False

    def append_data(self, counter, description, email, link, location, name, phone_number, services, sex):
        self.description.append(description)
        self.name.append(name)
        self.sex.append(sex)
        self.phone_number.append(phone_number)
        self.email.append(email)
        self.location.append(location)
        self.check_for_payment_methods(description)
        self.link.append(link)
        self.post_identifier.append(counter)
        self.services.append(services)

    def format_data_to_csv(self) -> None:
        titled_columns = {
            'Post-identifier': self.post_identifier,
            'Phone-Number': self.phone_number,
            'Link': self.link,
            'Location': self.location,
            'Name': self.name,
            'Sex': self.sex,
            'E-mail': self.email,
            'Services': self.services,
            'Description': self.description,
            'payment-methods': self.payment_methods_found,
            'keywords-found': self.keywords_found,
            'number-of-keywords-found': self.number_of_keywords_found
        }

        data = pd.DataFrame(titled_columns)
        data.to_csv(f'{self.scraper_directory}/yesbackpage-{self.date_time}.csv', index=False, sep="\t")

    def reset_variables(self) -> None:
        self.phone_number = []
        self.link = []
        self.name = []
        self.sex = []
        self.email = []
        self.location = []
        self.description = []
        self.post_identifier = []
        self.payment_methods_found = []
        self.services = []
        self.number_of_keywords_found = []
        self.keywords_found = []

    def check_for_payment_methods(self, description) -> None:
        payments = ''
        for payment in self.known_payment_methods:
            if payment in description.lower():
                payments += payment + '\n'

        if payments != '':
            self.payment_methods_found.append(payments)
        else:
            self.payment_methods_found.append('N/A')

    def capture_screenshot(self, screenshot_name) -> None:
        self.driver.save_screenshot(f'{self.screenshot_directory}/{screenshot_name}')

    def check_keywords(self, data) -> bool:
        for key in self.keywords:
            if key in data.lower():
                return True
        return False

    def check_and_append_keywords(self, data) -> None:
        for key in self.keywords:
            if key in data.lower():
                self.keywords_found_in_post.append(key)
                self.number_of_keywords_in_post += 1


# ---------------------------- Skipthegames ----------------------------

class SkipthegamesScraper(ScraperPrototype):
    def __init__(self):
        super().__init__()
        self.path = None
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
                                      'deposit', 'cc', 'card', 'credit card', 'applepay', 'donation', 'cash', 'visa',
                                      'paypal', 'mc', 'mastercard']

        self.date_time = None
        self.main_page_path = None
        self.screenshot_directory = None
        self.keywords = None

        self.join_keywords = False
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

    def get_cities(self) -> list:
        return list(self.cities.keys())

    def set_city(self, city) -> None:
        self.city = city

    def set_join_keywords(self) -> None:
        self.join_keywords = True

    def set_path(self, path) -> None:
        self.path = path

    def initialize(self, keywords) -> None:
        # set keywords value
        self.keywords = keywords

        # set up directories to save screenshots and csv file.
        self.date_time = str(datetime.today())[0:19].replace(' ', '_').replace(':', '-')

        # Format website URL based on state and city
        self.get_formatted_url()

        # Selenium Web Driver setup
        options = uc.ChromeOptions()
        # TODO - uncomment this to run headless
        # options.add_argument('--headless')
        self.driver = uc.Chrome(use_subprocess=True, options=options)

        # Open Webpage with URL
        self.open_webpage()

        # Find links of posts
        links = self.get_links()

        # create directories for screenshot and csv
        self.main_page_path = f'{self.path}/skipthegames_{self.date_time}'
        os.mkdir(self.main_page_path)
        self.screenshot_directory = f'{self.main_page_path}/screenshots'
        os.mkdir(self.screenshot_directory)

        self.get_data(links)
        self.format_data_to_csv()
        self.close_webpage()
        self.reset_variables()

    def open_webpage(self) -> None:
        self.driver.implicitly_wait(10)
        self.driver.get(self.url)
        self.driver.maximize_window()
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
        return set(links)

    def get_formatted_url(self) -> None:
        self.url = self.cities.get(self.city)

    def get_data(self, links) -> None:
        counter = 0

        for link in links:
            self.driver.get(link)
            assert "Page not found" not in self.driver.page_source

            try:
                about_info = self.driver.find_element(
                    By.XPATH, '/html/body/div[7]/div/div[2]/div/table/tbody').text
            except NoSuchElementException:
                about_info = 'N/A'

            try:
                services = self.driver.find_element(
                    By.XPATH, '//*[@id="post-services"]').text
            except NoSuchElementException:
                services = 'N/A'

            try:
                description = self.driver.find_element(
                    By.XPATH, '/html/body/div[7]/div/div[2]/div/div[1]/div').text
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

                    if self.join_keywords:
                        if len(self.keywords) == len(set(self.keywords_found_in_post)):
                            self.append_data(about_info, counter, description, link, services)

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
                        self.append_data(about_info, counter, description, link, services)

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
                self.append_data(about_info, counter, description, link, services)

                screenshot_name = str(counter) + ".png"
                self.capture_screenshot(screenshot_name)

                # append N/A if no keywords are found
                self.keywords_found.append('N/A')
                self.number_of_keywords_found.append('N/A')

                counter += 1

        self.join_keywords = False

    def append_data(self, about_info, counter, description, link, services):
        self.post_identifier.append(counter)
        self.link.append(link)
        self.about_info.append(about_info)
        self.services.append(services)
        self.description.append(description)
        self.check_for_payment_methods(description)

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

    def reset_variables(self) -> None:
        self.link = []
        self.about_info = []
        self.description = []
        self.services = []
        self.post_identifier = []
        self.payment_methods_found = []
        self.number_of_keywords_found = []
        self.keywords_found = []

    def check_for_payment_methods(self, description) -> None:
        payments = ''
        for payment in self.known_payment_methods:
            if payment in description.lower():
                payments += payment + ' '

        if payments != '':
            self.payment_methods_found.append(payments)
        else:
            self.payment_methods_found.append('N/A')

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
                self.number_of_keywords_in_post += 1


# ---------------------------- Megapersonals ----------------------------

class MegapersonalsScraper(ScraperPrototype):

    def __init__(self):
        super().__init__()
        self.path = None
        self.driver = None
        self.cities = {
            "daytona": 'https://megapersonals.eu/public/post_list/109/1/1',
            "fort lauderdale": 'https://megapersonals.eu/public/post_list/113/1/1',
            "fort myers": 'https://megapersonals.eu/public/post_list/234/1/1',
            "gainesville": 'https://megapersonals.eu/public/post_list/235/1/1',
            "jacksonville": 'https://megapersonals.eu/public/post_list/236/1/1',
            "keys": 'https://megapersonals.eu/public/post_list/114/1/1',
            "miami": 'https://megapersonals.eu/public/post_list/25/1/1',
            "ocala": 'https://megapersonals.eu/public/post_list/238/1/1',
            "okaloosa": 'https://megapersonals.eu/public/post_list/239/1/1',
            "orlando": 'https://megapersonals.eu/public/post_list/18/1/1',
            "palm bay": 'https://megapersonals.eu/public/post_list/110/1/1',
            "panama city": 'https://megapersonals.eu/public/post_list/240/1/1',
            "pensacola": 'https://megapersonals.eu/public/post_list/241/1/1',
            "sarasota": 'https://megapersonals.eu/public/post_list/242/1/1',
            "space coast": 'https://megapersonals.eu/public/post_list/111/1/1',
            "st. augustine": 'https://megapersonals.eu/public/post_list/243/1/1',
            "tallahassee": 'https://megapersonals.eu/public/post_list/244/1/1',
            "tampa": 'https://megapersonals.eu/public/post_list/50/1/1',
            "treasure coast": 'https://megapersonals.eu/public/post_list/112/1/1',
            "west palm beach": 'https://megapersonals.eu/public/post_list/115/1/1'
        }
        self.city = ''
        self.url = ''
        self.known_payment_methods = ['cashapp', 'venmo', 'zelle', 'crypto', 'western union', 'no deposit',
                                      'deposit', 'cc', 'card', 'credit card', 'applepay', 'donation', 'cash', 'visa',
                                      'paypal', 'mc', 'mastercard']

        # set date variables and path
        self.date_time = None
        self.main_page_path = None
        self.screenshot_directory = None
        self.keywords = None

        self.join_keywords = False
        self.number_of_keywords_in_post = 0
        self.keywords_found_in_post = []

        # lists to store data and then send to csv file
        self.description = []
        self.name = []
        self.phoneNumber = []
        self.contentCity = []
        self.location = []
        self.link = []
        self.post_identifier = []
        self.payment_methods_found = []

        self.number_of_keywords_found = []
        self.keywords_found = []

    def get_cities(self) -> list:
        return list(self.cities.keys())

    def set_city(self, city) -> None:
        self.city = city

    def set_join_keywords(self) -> None:
        self.join_keywords = True

    def set_path(self, path) -> None:
        self.path = path

    def initialize(self, keywords) -> None:
        # set keywords value
        self.keywords = keywords

        # format date
        self.date_time = str(datetime.today())[0:19].replace(' ', '_').replace(':', '-')

        # Format website URL based on state and city
        self.get_formatted_url()

        # Selenium Web Driver setup
        options = uc.ChromeOptions()
        # TODO - uncomment this to run headless
        # options.add_argument('--headless')
        self.driver = uc.Chrome(use_subprocess=True, options=options)

        # Open Webpage with URL
        self.open_webpage()

        # Find links of posts
        links = self.get_links()

        # create directories for screenshot and csv
        self.main_page_path = f'{self.path}/megapersonals_{self.date_time}'
        os.mkdir(self.main_page_path)
        self.screenshot_directory = f'{self.main_page_path}/screenshots'
        os.mkdir(self.screenshot_directory)

        self.get_data(links)
        self.format_data_to_csv()
        self.close_webpage()
        self.reset_variables()

    def open_webpage(self) -> None:
        self.driver.implicitly_wait(10)
        self.driver.get(self.url)
        self.driver.maximize_window()
        assert "Page not found" not in self.driver.page_source
        self.driver.find_element(By.CLASS_NAME, 'btn').click()
        self.driver.find_element(By.XPATH, '//*[@id="choseCityContainer"]/div[3]/label').click()
        self.driver.find_element(By.XPATH, '//*[@id="choseCityContainer"]/div[3]/article/div[10]/label').click()
        self.driver.find_element(By.XPATH,
                                 '//*[@id="choseCityContainer"]/div[3]/article/div[10]/article/p[3]/a').click()
        self.driver.find_element(By.XPATH, '//*[@id="megapCategoriesOrangeButton"]').click()

    def close_webpage(self) -> None:
        self.driver.close()

    def get_links(self) -> set:
        post_list = self.driver.find_elements(By.CLASS_NAME, 'listadd')

        # traverse through list of people to grab page links
        links = []
        for person in post_list:
            links.append(person.find_element(By.TAG_NAME, "a").get_attribute("href"))
        return set(links)

    def get_formatted_url(self):
        self.url = self.cities.get(self.city)

    def get_data(self, links) -> None:
        counter = 0

        for link in links:
            self.driver.get(link)
            assert "Page not found" not in self.driver.page_source

            try:
                description = self.driver.find_element(
                    By.XPATH, '/html/body/div/div[6]/span').text
            except NoSuchElementException:
                description = 'N/A'

            try:
                phone_number = self.driver.find_element(
                    By.XPATH, '/html/body/div/div[6]/div[1]/span').text
            except NoSuchElementException:
                phone_number = 'N/A'

            try:
                name = self.driver.find_element(
                    By.XPATH, '/html/body/div/div[6]/p[1]/span[2]').text[5:]
            except NoSuchElementException:
                name = 'N/A'

            try:
                city = self.driver.find_element(
                    By.XPATH, '/html/body/div/div[6]/p[1]/span[1]').text[5:]
            except NoSuchElementException:
                city = 'N/A'

            try:
                location = self.driver.find_element(
                    By.XPATH, '/html/body/div/div[6]/p[2]').text[9:]
            except NoSuchElementException:
                location = 'N/A'

            # reassign variables for each post
            self.number_of_keywords_in_post = 0
            self.keywords_found_in_post = []

            if len(self.keywords) > 0:
                if self.check_keywords(description) or self.check_keywords(name) \
                        or self.check_keywords(phone_number) or self.check_keywords(city) \
                        or self.check_keywords(location):

                    # check for keywords and append to lists
                    self.check_and_append_keywords(description)
                    self.check_and_append_keywords(name)
                    self.check_and_append_keywords(phone_number)
                    self.check_and_append_keywords(city)
                    self.check_and_append_keywords(location)

                    if self.join_keywords:
                        if len(self.keywords) == len(set(self.keywords_found_in_post)):
                            self.append_data(city, counter, description, link, location, name, phone_number)

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
                        self.append_data(city, counter, description, link, location, name, phone_number)

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
                self.append_data(city, counter, description, link, location, name, phone_number)

                screenshot_name = str(counter) + ".png"
                self.capture_screenshot(screenshot_name)

                # append N/A if no keywords are found
                self.keywords_found.append('N/A')
                self.number_of_keywords_found.append('N/A')

                counter += 1

        self.join_keywords = False

    def append_data(self, city, counter, description, link, location, name, phone_number):
        self.post_identifier.append(counter)
        self.name.append(name)
        self.phoneNumber.append(phone_number)
        self.contentCity.append(city)
        self.location.append(location)
        self.description.append(description)
        self.check_for_payment_methods(description)
        self.link.append(link)

    def format_data_to_csv(self) -> None:
        titled_columns = {
            'Post-identifier': self.post_identifier,
            'Link': self.link,
            'name': self.name,
            'phone-number': self.phoneNumber,
            'city': self.contentCity,
            'location': self.location,
            'description': self.description,
            'payment-methods': self.payment_methods_found,
            'keywords-found': self.keywords_found,
            'number-of-keywords-found': self.number_of_keywords_found
        }

        data = pd.DataFrame(titled_columns)
        data.to_csv(f'{self.main_page_path}/megapersonals-{self.date_time}.csv', index=False, sep="\t")

    def reset_variables(self) -> None:
        self.description = []
        self.name = []
        self.phoneNumber = []
        self.contentCity = []
        self.location = []
        self.link = []
        self.post_identifier = []
        self.payment_methods_found = []
        self.number_of_keywords_found = []
        self.keywords_found = []

    def check_for_payment_methods(self, description) -> None:
        payments = ''
        for payment in self.known_payment_methods:
            if payment in description.lower():
                payments += payment + ' '

        if payments != '':
            self.payment_methods_found.append(payments)
        else:
            self.payment_methods_found.append('N/A')

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
                self.number_of_keywords_in_post += 1


# ---------------------------- Escort Alligator ----------------------------

class EscortalligatorScraper(ScraperPrototype):
    def __init__(self):
        super().__init__()
        self.path = None
        self.driver = None

        self.cities = [
            "daytona",
            "fort lauderdale",
            "fort myers",
            "gainesville",
            "jacksonville",
            "keys",
            "miami",
            "ocala",
            "okaloosa",
            "orlando",
            "palm bay",
            "panama city",
            "pensacola",
            "bradenton",
            "space coast",
            "st. augustine",
            "tallahassee",
            "tampa",
            "treasure coast",
            "west palm beach",
            "jacksonville"
        ]
        self.city = ''
        self.state = 'florida'
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

        # lists to store data and then send to csv file
        self.phone_number = []
        self.description = []
        self.location_and_age = []
        self.links = []
        self.post_identifier = []
        self.payment_methods_found = []

        self.number_of_keywords_found = []
        self.keywords_found = []

    def get_cities(self) -> list:
        return self.cities

    def set_city(self, city) -> None:
        self.city = city.replace(' ', '').replace('.', '')

    def set_join_keywords(self) -> None:
        self.join_keywords = True

    def set_path(self, path) -> None:
        self.path = path

    def initialize(self, keywords) -> None:
        # set keywords value
        self.keywords = keywords

        self.date_time = str(datetime.today())[0:19].replace(' ', '_').replace(':', '-')

        # Format website URL based on state and city
        self.get_formatted_url()

        # Selenium Web Driver setup
        options = uc.ChromeOptions()
        # TODO - uncomment this to run headless
        # options.add_argument('--headless')
        self.driver = uc.Chrome(subprocess=True, options=options)

        # Open Webpage with URL
        self.open_webpage()

        # Find links of posts
        links = self.get_links()

        # Create directory for search data
        self.scraper_directory = f'{self.path}/escortalligator_{self.date_time}'
        os.mkdir(self.scraper_directory)

        # Create directory for search screenshots
        self.screenshot_directory = f'{self.scraper_directory}/screenshots'
        os.mkdir(self.screenshot_directory)

        # Get data from posts
        self.get_data(links)
        self.close_webpage()
        self.format_data_to_csv()
        self.reset_variables()

    def open_webpage(self) -> None:
        self.driver.implicitly_wait(10)
        self.driver.get(self.url)
        self.driver.maximize_window()
        assert "Page not found" not in self.driver.page_source

    def close_webpage(self) -> None:
        self.driver.close()

    def get_links(self) -> list:
        # click on terms btn
        btn = self.driver.find_element(
            By.CLASS_NAME, 'button')
        btn.click()

        time.sleep(2)
        # click on 2nd terms btn
        btn = self.driver.find_element(
            By.CLASS_NAME, 'footer')
        btn.click()

        posts = self.driver.find_elements(
            By.CSS_SELECTOR, '#list [href]')
        links = [post.get_attribute('href') for post in posts]
        return links[::3]

    def get_formatted_url(self) -> None:
        self.url = f'https://escortalligator.com.listcrawler.eu/brief/escorts/usa/{self.state}/{self.city}/1'

    def get_data(self, links) -> None:
        links = set(links)
        counter = 0

        for link in links:
            self.driver.get(link)
            assert "Page not found" not in self.driver.page_source

            try:
                description = self.driver.find_element(
                    By.CLASS_NAME, 'viewpostbody').text
            except NoSuchElementException:
                description = 'N/A'

            try:
                phone_number = self.driver.find_element(
                    By.CLASS_NAME, 'userInfoContainer').text
            except NoSuchElementException:
                phone_number = 'N/A'

            try:
                location_and_age = self.driver.find_element(
                    By.CLASS_NAME, 'viewpostlocationIconBabylon').text
            except NoSuchElementException:
                location_and_age = 'N/A'

            # reassign variables for each post
            self.number_of_keywords_in_post = 0
            self.keywords_found_in_post = []

            if len(self.keywords) > 0:
                if self.check_keywords(phone_number) or self.check_keywords(location_and_age) or \
                        self.check_keywords(description):

                    # check for keywords and append to lists
                    self.check_and_append_keywords(phone_number)
                    self.check_and_append_keywords(location_and_age)
                    self.check_and_append_keywords(description)

                    if self.join_keywords:
                        if len(self.keywords) == len(set(self.keywords_found_in_post)):

                            self.append_data(counter, description, link, location_and_age, phone_number)

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
                        self.append_data(counter, description, link, location_and_age, phone_number)
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
                self.append_data(counter, description, link, location_and_age, phone_number)

                screenshot_name = str(counter) + ".png"
                self.capture_screenshot(screenshot_name)

                # append N/A if no keywords are found
                self.keywords_found.append('N/A')
                self.number_of_keywords_found.append('N/A')

                counter += 1

        self.join_keywords = False

    def append_data(self, counter, description, link, location_and_age, phone_number) -> None:
        self.post_identifier.append(counter)
        self.phone_number.append(phone_number)
        self.links.append(link)
        self.location_and_age.append(location_and_age)
        self.description.append(description)
        self.check_for_payment_methods(description)

    def format_data_to_csv(self) -> None:
        titled_columns = {
            'Post-identifier': self.post_identifier,
            'Phone-Number': self.phone_number,
            'Link': self.links,
            'Location/Age': self.location_and_age,
            'Description': self.description,
            'payment-methods': self.payment_methods_found,
            'keywords-found': self.keywords_found,
            'number-of-keywords-found': self.number_of_keywords_found
        }

        data = pd.DataFrame(titled_columns)
        data.to_csv(f'{self.scraper_directory}/escortalligator-{self.date_time}.csv', index=False, sep="\t")

    def reset_variables(self) -> None:
        self.phone_number = []
        self.description = []
        self.location_and_age = []
        self.links = []
        self.post_identifier = []
        self.payment_methods_found = []
        self.number_of_keywords_found = []
        self.keywords_found = []

    def check_for_payment_methods(self, description) -> None:
        payments = ''
        for payment in self.known_payment_methods:
            if payment in description.lower():
                payments += payment + ' '

        if payments != '':
            self.payment_methods_found.append(payments)
        else:
            self.payment_methods_found.append('N/A')

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
                self.number_of_keywords_in_post += 1


# ----------------------------- Eros ----------------------------

class ErosScraper(ScraperPrototype):
    def __init__(self):
        super().__init__()
        self.path = None
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

    def get_cities(self) -> list:
        return list(self.cities.keys())

    def set_city(self, city) -> None:
        self.city = city

    def set_join_keywords(self) -> None:
        self.join_keywords = True

    def set_path(self, path) -> None:
        self.path = path

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
        self.scraper_directory = f'{self.path}/eros_{self.date_time}'
        os.mkdir(self.scraper_directory)

        # Create directory for search screenshots
        self.screenshot_directory = f'{self.scraper_directory}/screenshots'
        os.mkdir(self.screenshot_directory)

        # Get data from posts
        self.get_data(links)
        self.close_webpage()
        self.format_data_to_csv()
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
            exit(1)

        try:
            # Find all profile links
            posts = self.driver.find_elements(
                By.CSS_SELECTOR, '#listing > div.grid.fourPerRow.mobile.switchable [href]')
        except NoSuchElementException:
            exit(1)

        if posts:
            links = [post.get_attribute('href') for post in posts]
        else:
            exit(1)

        return set(links)

    def get_formatted_url(self) -> None:
        self.url = self.cities.get(self.city)

    def get_data(self, links) -> None:
        description = ''
        counter = 0

        for link in links:
            self.driver.implicitly_wait(10)
            self.driver.get(link)
            assert "Page not found" not in self.driver.page_source

            try:
                profile_header = self.driver.find_element(
                    By.XPATH, '//*[@id="pageone"]/div[1]').text
            except NoSuchElementException:
                profile_header = 'N/A'

            try:
                description = self.driver.find_element(
                    By.XPATH, '// *[ @ id = "pageone"] / div[3] / div / div[1] / div[2]').text
            except NoSuchElementException:
                description = 'N/A'

            try:
                info_details = self.driver.find_element(
                    By.XPATH, '//*[@id="pageone"]/div[3]/div/div[2]/div[1]/div').text
            except NoSuchElementException:
                info_details = 'N/A'

            try:
                contact_details = self.driver.find_element(
                    By.XPATH, '//*[@id="pageone"]/div[3]/div/div[2]/div[2]').text
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

                    if self.join_keywords:
                        if len(self.keywords) == len(set(self.keywords_found_in_post)):

                            self.append_data(contact_details, counter, description, info_details, link, profile_header)

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
                        self.append_data(contact_details, counter, description, info_details, link, profile_header)

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
                self.append_data(contact_details, counter, description, info_details, link, profile_header)

                screenshot_name = str(counter) + ".png"
                self.capture_screenshot(screenshot_name)

                # append N/A if no keywords are found
                self.keywords_found.append('N/A')
                self.number_of_keywords_found.append('N/A')

                counter += 1
            if counter == 3:
                break

        self.join_keywords = False

    def append_data(self, contact_details, counter, description, info_details, link, profile_header) -> None:
        self.post_identifier.append(counter)
        self.link.append(link)
        self.profile_header.append(profile_header)
        self.about_info.append(description)
        self.info_details.append(info_details)
        self.contact_details.append(contact_details)
        self.check_for_payment_methods(description)

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

    def reset_variables(self) -> None:
        self.post_identifier = []
        self.link = []
        self.profile_header = []
        self.about_info = []
        self.info_details = []
        self.contact_details = []
        self.payment_methods_found = []
        self.number_of_keywords_found = []
        self.keywords_found = []

    def check_for_payment_methods(self, description) -> None:
        payments = ''
        for payment in self.known_payment_methods:
            if payment in description.lower():
                payments += payment + ' '

        if payments != '':
            self.payment_methods_found.append(payments)
        else:
            self.payment_methods_found.append('N/A')

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
                self.number_of_keywords_in_post += 1


# ---------------------------- Keywords ----------------------------
class Keywords:
    def __init__(self):
        self.keywords = []
        self.sets = {}
        self.keywords_path = ''
        self.keywords_set_path = ''

    def set_keywords_path(self, keyword_file_path):
        self.keywords_path = keyword_file_path

    def set_keywords_sets_path(self, keyword_sets_file_path):
        self.keywords_set_path = keyword_sets_file_path

    def add_keywords(self, keyword):
        # self.keywords.append(keyword)
        if self.keywords_path != '':
            with open(self.keywords_path, "r+") as filename:
                content_set = filename.read().splitlines()
                if keyword not in content_set:
                    filename.write("\n" + keyword.lower())

    def remove_keywords(self, keyword):
        # self.keywords.remove(keyword)
        if self.keywords_path != '':
            with open(self.keywords_path, "r") as filename:
                content_set = filename.read().splitlines()
                index = content_set.index(keyword.lower())

                content_set.remove(content_set[index])

            with open(self.keywords_path, "w") as filename:
                filename.write("\n".join(content_set))

    def create_set(self, set_name, keywords_list):
        # self.sets[set_name.lower()] = keywords_list

        if self.keywords_set_path != '':
            with open(self.keywords_set_path, "r") as readfile:
                read = readfile.read()
                if read != '':
                    self.sets = json.loads(read)
            self.sets[set_name.lower()] = keywords_list
            with open(self.keywords_set_path, "w") as writefile:
                json.dump(self.sets, writefile)

    def remove_set(self, set_name):
        # del self.sets[set_name.lower()]

        if self.keywords_set_path != '':
            with open(self.keywords_set_path, "r") as readfile:
                self.sets = json.loads(readfile.read())

            del self.sets[set_name.lower()]

            with open(self.keywords_set_path, 'w') as writefile:
                json.dump(self.sets, writefile)

    def get_set_values(self, set_name):
        if self.keywords_set_path != '':
            with open(self.keywords_set_path, "r") as readfile:
                self.sets = json.loads(readfile.read())

            return self.sets[set_name.lower()]

    def get_keywords(self):
        if self.keywords_path != '':
            with open(self.keywords_path, "r") as filename:
                self.keywords = filename.read().splitlines()

            return self.keywords

    def get_set(self):
        if self.keywords_set_path != '':
            with open(self.keywords_set_path, "r") as filename:
                self.sets = json.loads(filename.read())

            return self.sets

    def remove_keyword_from_set(self, keyword, set_name):
        if self.keywords_set_path != '':
            with open(self.keywords_set_path, "r") as readfile:
                self.sets = json.loads(readfile.read())

            list_value = list(self.sets[set_name])
            list_value.remove(keyword)
            self.sets[set_name] = list_value

            with open(self.keywords_set_path, "w") as writefile:
                json.dump(self.sets, writefile)


# ---------------------------- Facade ----------------------------
class Facade:
    def __init__(self):
        self.eros = ErosScraper()
        self.escortalligator = EscortalligatorScraper()
        self.yesbackpage = YesbackpageScraper()
        self.megapersonals = MegapersonalsScraper()
        self.skipthegames = SkipthegamesScraper()

    def initialize_escortalligator_scraper(self, keywords):
        self.escortalligator.initialize(keywords)

    def set_escortalligator_city(self, city):
        self.escortalligator.set_city(city)

    def set_escortalligator_join_keywords(self):
        self.escortalligator.set_join_keywords()

    def get_escortalligator_cities(self):
        return self.escortalligator.get_cities()

    def initialize_megapersonals_scraper(self, keywords):
        self.megapersonals.initialize(keywords)

    def set_megapersonals_city(self, city):
        self.megapersonals.set_city(city)

    def set_megapersonals_join_keywords(self):
        self.megapersonals.set_join_keywords()

    def get_megapersonals_cities(self):
        self.megapersonals = MegapersonalsScraper()
        return self.megapersonals.get_cities()

    def initialize_skipthegames_scraper(self, keywords):
        self.skipthegames.initialize(keywords)

    def set_skipthegames_city(self, city):
        self.skipthegames.set_city(city)

    def set_skipthegames_join_keywords(self):
        self.skipthegames.set_join_keywords()

    def get_skipthegames_cities(self):
        return self.skipthegames.get_cities()

    def initialize_yesbackpage_scraper(self, keywords):
        self.yesbackpage.initialize(keywords)

    def set_yesbackpage_city(self, city):
        self.yesbackpage.set_city(city)

    def set_yesbackpage_join_keywords(self):
        self.yesbackpage.set_join_keywords()

    def get_yesbackpage_cities(self):
        return self.yesbackpage.get_cities()

    def initialize_eros_scraper(self, keywords):
        self.eros.initialize(keywords)

    def set_eros_city(self, city):
        self.eros.set_city(city)

    def set_eros_join_keywords(self):
        self.eros.set_join_keywords()

    def get_eros_cities(self):
        return self.eros.get_cities()

    def format_data(self, data):
        pass

    def set_storage_path(self, file_storage_path):
        if file_storage_path != '':
            self.yesbackpage.set_path(file_storage_path)
            self.skipthegames.set_path(file_storage_path)
            self.megapersonals.set_path(file_storage_path)
            self.escortalligator.set_path(file_storage_path)
            self.eros.set_path(file_storage_path)


# ---------------------------- Scraper (created using .ui file) ----------------------------
# Form implementation generated from reading ui file 'Scraper.ui'
# Created by: PyQt6 UI code generator 6.4.2

'''WARNING: Any manual changes made to this file will be lost when pyuic6 is
run again.  Do not edit this file unless you know what you are doing.'''

class Ui_HSIWebScraper(object):
    def setupUi(self, HSIWebScraper):
        HSIWebScraper.setObjectName("HSIWebScraper")
        HSIWebScraper.resize(1126, 688)
        self.tabWidget = QtWidgets.QTabWidget(parent=HSIWebScraper)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1131, 691))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.tabWidget.setFont(font)
        self.tabWidget.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.setFileSelectionButton = QtWidgets.QPushButton(parent=self.tab)
        self.setFileSelectionButton.setGeometry(QtCore.QRect(440, 350, 221, 41))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.setFileSelectionButton.setFont(font)
        self.setFileSelectionButton.setObjectName("setFileSelectionButton")
        self.keywordfileSelectionButton = QtWidgets.QPushButton(parent=self.tab)
        self.keywordfileSelectionButton.setGeometry(QtCore.QRect(440, 190, 221, 41))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.keywordfileSelectionButton.setFont(font)
        self.keywordfileSelectionButton.setObjectName("keywordfileSelectionButton")
        self.selectKeywordFilesLabel = QtWidgets.QLabel(parent=self.tab)
        self.selectKeywordFilesLabel.setGeometry(QtCore.QRect(440, 110, 221, 31))
        self.selectKeywordFilesLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.selectKeywordFilesLabel.setObjectName("selectKeywordFilesLabel")
        self.label = QtWidgets.QLabel(parent=self.tab)
        self.label.setGeometry(QtCore.QRect(300, 420, 511, 41))
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.storagePathSelectionButton = QtWidgets.QPushButton(parent=self.tab)
        self.storagePathSelectionButton.setGeometry(QtCore.QRect(440, 510, 221, 41))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.storagePathSelectionButton.setFont(font)
        self.storagePathSelectionButton.setObjectName("storagePathSelectionButton")
        self.keywordFilePathOutput = QtWidgets.QTextBrowser(parent=self.tab)
        self.keywordFilePathOutput.setGeometry(QtCore.QRect(440, 150, 221, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.keywordFilePathOutput.setFont(font)
        self.keywordFilePathOutput.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.keywordFilePathOutput.setLineWrapMode(QtWidgets.QTextEdit.LineWrapMode.NoWrap)
        self.keywordFilePathOutput.setObjectName("keywordFilePathOutput")
        self.keywordSetsPathOutput = QtWidgets.QTextBrowser(parent=self.tab)
        self.keywordSetsPathOutput.setGeometry(QtCore.QRect(440, 310, 221, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.keywordSetsPathOutput.setFont(font)
        self.keywordSetsPathOutput.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.keywordSetsPathOutput.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.keywordSetsPathOutput.setLineWrapMode(QtWidgets.QTextEdit.LineWrapMode.NoWrap)
        self.keywordSetsPathOutput.setObjectName("keywordSetsPathOutput")
        self.storagePathOutput = QtWidgets.QTextBrowser(parent=self.tab)
        self.storagePathOutput.setGeometry(QtCore.QRect(440, 470, 221, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.storagePathOutput.setFont(font)
        self.storagePathOutput.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.storagePathOutput.setLineWrapMode(QtWidgets.QTextEdit.LineWrapMode.NoWrap)
        self.storagePathOutput.setObjectName("storagePathOutput")
        self.label_3 = QtWidgets.QLabel(parent=self.tab)
        self.label_3.setGeometry(QtCore.QRect(290, 30, 521, 61))
        font = QtGui.QFont()
        font.setPointSize(25)
        font.setBold(True)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.selectKeywordFilesLabel_2 = QtWidgets.QLabel(parent=self.tab)
        self.selectKeywordFilesLabel_2.setGeometry(QtCore.QRect(410, 260, 291, 41))
        self.selectKeywordFilesLabel_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.selectKeywordFilesLabel_2.setObjectName("selectKeywordFilesLabel_2")
        self.keywordFileProgressBar = QtWidgets.QProgressBar(parent=self.tab)
        self.keywordFileProgressBar.setGeometry(QtCore.QRect(440, 230, 221, 16))
        font = QtGui.QFont()
        font.setPointSize(1)
        self.keywordFileProgressBar.setFont(font)
        self.keywordFileProgressBar.setProperty("value", 0)
        self.keywordFileProgressBar.setTextVisible(False)
        self.keywordFileProgressBar.setObjectName("keywordFileProgressBar")
        self.keywordSetsProgressBar = QtWidgets.QProgressBar(parent=self.tab)
        self.keywordSetsProgressBar.setGeometry(QtCore.QRect(440, 390, 221, 16))
        font = QtGui.QFont()
        font.setPointSize(1)
        self.keywordSetsProgressBar.setFont(font)
        self.keywordSetsProgressBar.setProperty("value", 0)
        self.keywordSetsProgressBar.setTextVisible(False)
        self.keywordSetsProgressBar.setObjectName("keywordSetsProgressBar")
        self.storagePathProgressBar = QtWidgets.QProgressBar(parent=self.tab)
        self.storagePathProgressBar.setGeometry(QtCore.QRect(440, 550, 221, 16))
        font = QtGui.QFont()
        font.setPointSize(1)
        self.storagePathProgressBar.setFont(font)
        self.storagePathProgressBar.setProperty("value", 0)
        self.storagePathProgressBar.setTextVisible(False)
        self.storagePathProgressBar.setObjectName("storagePathProgressBar")
        self.label_5 = QtWidgets.QLabel(parent=self.tab)
        self.label_5.setGeometry(QtCore.QRect(1000, 600, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.tabWidget.addTab(self.tab, "")
        self.MainScraper = QtWidgets.QWidget()
        self.MainScraper.setToolTipDuration(-1)
        self.MainScraper.setObjectName("MainScraper")
        self.keywordlistWidget = QtWidgets.QListWidget(parent=self.MainScraper)
        self.keywordlistWidget.setGeometry(QtCore.QRect(610, 180, 321, 221))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.keywordlistWidget.setFont(font)
        self.keywordlistWidget.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.MultiSelection)
        self.keywordlistWidget.setObjectName("keywordlistWidget")
        self.setSelectionDropdown = QtWidgets.QComboBox(parent=self.MainScraper)
        self.setSelectionDropdown.setGeometry(QtCore.QRect(200, 370, 231, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.setSelectionDropdown.setFont(font)
        self.setSelectionDropdown.setCurrentText("")
        self.setSelectionDropdown.setObjectName("setSelectionDropdown")
        self.setSelectionDropdown.addItem("")
        self.setSelectionDropdown.setItemText(0, "")
        self.setSelectionLabel = QtWidgets.QLabel(parent=self.MainScraper)
        self.setSelectionLabel.setGeometry(QtCore.QRect(190, 330, 361, 31))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.setSelectionLabel.setFont(font)
        self.setSelectionLabel.setObjectName("setSelectionLabel")
        self.keywordListLabel = QtWidgets.QLabel(parent=self.MainScraper)
        self.keywordListLabel.setGeometry(QtCore.QRect(610, 145, 211, 31))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.keywordListLabel.setFont(font)
        self.keywordListLabel.setObjectName("keywordListLabel")
        self.searchButton = QtWidgets.QPushButton(parent=self.MainScraper)
        self.searchButton.setGeometry(QtCore.QRect(500, 550, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(17)
        font.setBold(True)
        self.searchButton.setFont(font)
        self.searchButton.setObjectName("searchButton")
        self.keywordInclusivecheckBox = QtWidgets.QCheckBox(parent=self.MainScraper)
        self.keywordInclusivecheckBox.setGeometry(QtCore.QRect(610, 480, 351, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.keywordInclusivecheckBox.setFont(font)
        self.keywordInclusivecheckBox.setObjectName("keywordInclusivecheckBox")
        self.textSearchLabel = QtWidgets.QLabel(parent=self.MainScraper)
        self.textSearchLabel.setGeometry(QtCore.QRect(180, 420, 331, 41))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.textSearchLabel.setFont(font)
        self.textSearchLabel.setObjectName("textSearchLabel")
        self.HSIScraperlabel = QtWidgets.QLabel(parent=self.MainScraper)
        self.HSIScraperlabel.setGeometry(QtCore.QRect(350, 10, 411, 101))
        font = QtGui.QFont()
        font.setPointSize(36)
        font.setBold(True)
        self.HSIScraperlabel.setFont(font)
        self.HSIScraperlabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.HSIScraperlabel.setObjectName("HSIScraperlabel")
        self.websiteSelectionDropdown = QtWidgets.QComboBox(parent=self.MainScraper)
        self.websiteSelectionDropdown.setGeometry(QtCore.QRect(200, 190, 231, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.websiteSelectionDropdown.setFont(font)
        self.websiteSelectionDropdown.setCurrentText("")
        self.websiteSelectionDropdown.setObjectName("websiteSelectionDropdown")
        self.websiteSelectionDropdown.addItem("")
        self.websiteSelectionDropdown.setItemText(0, "")
        self.websiteSelectionDropdown.addItem("")
        self.websiteSelectionDropdown.addItem("")
        self.websiteSelectionDropdown.addItem("")
        self.websiteSelectionDropdown.addItem("")
        self.websiteSelectionDropdown.addItem("")
        self.websiteSelectionLabel = QtWidgets.QLabel(parent=self.MainScraper)
        self.websiteSelectionLabel.setGeometry(QtCore.QRect(190, 155, 291, 31))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.websiteSelectionLabel.setFont(font)
        self.websiteSelectionLabel.setObjectName("websiteSelectionLabel")
        self.searchTextBox = QtWidgets.QLineEdit(parent=self.MainScraper)
        self.searchTextBox.setGeometry(QtCore.QRect(200, 460, 231, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.searchTextBox.setFont(font)
        self.searchTextBox.setText("")
        self.searchTextBox.setObjectName("searchTextBox")
        self.selectAllKeywordscheckBox = QtWidgets.QCheckBox(parent=self.MainScraper)
        self.selectAllKeywordscheckBox.setGeometry(QtCore.QRect(610, 410, 361, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.selectAllKeywordscheckBox.setFont(font)
        self.selectAllKeywordscheckBox.setObjectName("selectAllKeywordscheckBox")
        self.paymentMethodcheckBox = QtWidgets.QCheckBox(parent=self.MainScraper)
        self.paymentMethodcheckBox.setGeometry(QtCore.QRect(610, 440, 481, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.paymentMethodcheckBox.setFont(font)
        self.paymentMethodcheckBox.setObjectName("paymentMethodcheckBox")
        self.setlocationDropdown = QtWidgets.QComboBox(parent=self.MainScraper)
        self.setlocationDropdown.setGeometry(QtCore.QRect(200, 280, 231, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.setlocationDropdown.setFont(font)
        self.setlocationDropdown.setCurrentText("")
        self.setlocationDropdown.setObjectName("setlocationDropdown")
        self.setLocationLabel = QtWidgets.QLabel(parent=self.MainScraper)
        self.setLocationLabel.setGeometry(QtCore.QRect(190, 240, 291, 31))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.setLocationLabel.setFont(font)
        self.setLocationLabel.setObjectName("setLocationLabel")
        self.label_6 = QtWidgets.QLabel(parent=self.MainScraper)
        self.label_6.setGeometry(QtCore.QRect(1000, 600, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.tabWidget.addTab(self.MainScraper, "")
        self.EditKeywords = QtWidgets.QWidget()
        self.EditKeywords.setObjectName("EditKeywords")
        self.setList = QtWidgets.QListWidget(parent=self.EditKeywords)
        self.setList.setGeometry(QtCore.QRect(660, 230, 311, 181))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.setList.setFont(font)
        self.setList.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.setList.setObjectName("setList")
        self.newSetTextBox = QtWidgets.QLineEdit(parent=self.EditKeywords)
        self.newSetTextBox.setGeometry(QtCore.QRect(660, 189, 191, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.newSetTextBox.setFont(font)
        self.newSetTextBox.setObjectName("newSetTextBox")
        self.addKeywordButton = QtWidgets.QPushButton(parent=self.EditKeywords)
        self.addKeywordButton.setGeometry(QtCore.QRect(330, 169, 131, 32))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.addKeywordButton.setFont(font)
        self.addKeywordButton.setObjectName("addKeywordButton")
        self.newKeywordTextBox = QtWidgets.QLineEdit(parent=self.EditKeywords)
        self.newKeywordTextBox.setGeometry(QtCore.QRect(150, 169, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.newKeywordTextBox.setFont(font)
        self.newKeywordTextBox.setObjectName("newKeywordTextBox")
        self.keywordList = QtWidgets.QListWidget(parent=self.EditKeywords)
        self.keywordList.setGeometry(QtCore.QRect(150, 210, 311, 201))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.keywordList.setFont(font)
        self.keywordList.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.MultiSelection)
        self.keywordList.setObjectName("keywordList")
        self.removeKeywordButton = QtWidgets.QPushButton(parent=self.EditKeywords)
        self.removeKeywordButton.setGeometry(QtCore.QRect(200, 420, 221, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.removeKeywordButton.setFont(font)
        self.removeKeywordButton.setObjectName("removeKeywordButton")
        self.newKeywordLabel = QtWidgets.QLabel(parent=self.EditKeywords)
        self.newKeywordLabel.setGeometry(QtCore.QRect(140, 135, 211, 31))
        self.newKeywordLabel.setObjectName("newKeywordLabel")
        self.newSetLabel = QtWidgets.QLabel(parent=self.EditKeywords)
        self.newSetLabel.setGeometry(QtCore.QRect(660, 154, 261, 31))
        self.newSetLabel.setObjectName("newSetLabel")
        self.addSetButton = QtWidgets.QPushButton(parent=self.EditKeywords)
        self.addSetButton.setGeometry(QtCore.QRect(870, 189, 101, 32))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.addSetButton.setFont(font)
        self.addSetButton.setObjectName("addSetButton")
        self.removeSetButton = QtWidgets.QPushButton(parent=self.EditKeywords)
        self.removeSetButton.setGeometry(QtCore.QRect(720, 419, 191, 32))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.removeSetButton.setFont(font)
        self.removeSetButton.setObjectName("removeSetButton")
        self.newSetLabel_2 = QtWidgets.QLabel(parent=self.EditKeywords)
        self.newSetLabel_2.setGeometry(QtCore.QRect(660, 120, 411, 31))
        self.newSetLabel_2.setObjectName("newSetLabel_2")
        self.label_2 = QtWidgets.QLabel(parent=self.EditKeywords)
        self.label_2.setGeometry(QtCore.QRect(90, 470, 451, 61))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_4 = QtWidgets.QLabel(parent=self.EditKeywords)
        self.label_4.setGeometry(QtCore.QRect(260, 10, 591, 81))
        font = QtGui.QFont()
        font.setPointSize(25)
        font.setBold(True)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.label_7 = QtWidgets.QLabel(parent=self.EditKeywords)
        self.label_7.setGeometry(QtCore.QRect(1000, 600, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.tabWidget.addTab(self.EditKeywords, "")

        self.retranslateUi(HSIWebScraper)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(HSIWebScraper)

    def retranslateUi(self, HSIWebScraper):
        _translate = QtCore.QCoreApplication.translate
        HSIWebScraper.setWindowTitle(_translate("HSIWebScraper", "NetSpider"))
        self.setFileSelectionButton.setText(_translate("HSIWebScraper", "Select keyword_sets.txt"))
        self.keywordfileSelectionButton.setText(_translate("HSIWebScraper", "Select keywords.txt"))
        self.selectKeywordFilesLabel.setText(_translate("HSIWebScraper", "Select keyword file:"))
        self.label.setText(_translate("HSIWebScraper", "Select folder to store screenshots and csv file:"))
        self.storagePathSelectionButton.setText(_translate("HSIWebScraper", "Select folder to store files"))
        self.keywordFilePathOutput.setPlaceholderText(_translate("HSIWebScraper", "No file chosen"))
        self.keywordSetsPathOutput.setPlaceholderText(_translate("HSIWebScraper", "No file chosen"))
        self.storagePathOutput.setPlaceholderText(_translate("HSIWebScraper", "No folder chosen"))
        self.label_3.setText(_translate("HSIWebScraper", "Choose file settings for scraper."))
        self.selectKeywordFilesLabel_2.setText(_translate("HSIWebScraper", "Select keyword sets file:"))
        self.label_5.setText(_translate("HSIWebScraper", "NetSpider v1.0.0"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("HSIWebScraper", "Settings"))
        self.setSelectionLabel.setText(_translate("HSIWebScraper", "  Select set of keywords (optional):"))
        self.keywordListLabel.setText(_translate("HSIWebScraper", "List of keywords:"))
        self.searchButton.setText(_translate("HSIWebScraper", "Search"))
        self.keywordInclusivecheckBox.setText(_translate("HSIWebScraper", "Keyword inclusive search (AND)."))
        self.textSearchLabel.setText(_translate("HSIWebScraper", "   Type text to scrape (optional):"))
        self.HSIScraperlabel.setText(_translate("HSIWebScraper", "Web Scraper"))
        self.websiteSelectionDropdown.setItemText(1, _translate("HSIWebScraper", "escortalligator"))
        self.websiteSelectionDropdown.setItemText(2, _translate("HSIWebScraper", "megapersonals"))
        self.websiteSelectionDropdown.setItemText(3, _translate("HSIWebScraper", "skipthegames"))
        self.websiteSelectionDropdown.setItemText(4, _translate("HSIWebScraper", "yesbackpage"))
        self.websiteSelectionDropdown.setItemText(5, _translate("HSIWebScraper", "eros"))
        self.websiteSelectionLabel.setText(_translate("HSIWebScraper", "  Select website to scrape:"))
        self.searchTextBox.setPlaceholderText(_translate("HSIWebScraper", " Type text to search here. "))
        self.selectAllKeywordscheckBox.setText(_translate("HSIWebScraper", "Select all keywords from list."))
        self.paymentMethodcheckBox.setText(_translate("HSIWebScraper", "Find only posts with payment methods."))
        self.setLocationLabel.setText(_translate("HSIWebScraper", "  Select location:"))
        self.label_6.setText(_translate("HSIWebScraper", "NetSpider v1.0.0"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.MainScraper), _translate("HSIWebScraper", "Scraper"))
        self.newSetTextBox.setPlaceholderText(_translate("HSIWebScraper", " Type new set name."))
        self.addKeywordButton.setText(_translate("HSIWebScraper", "Add keyword"))
        self.newKeywordTextBox.setPlaceholderText(_translate("HSIWebScraper", " Type new keyword."))
        self.removeKeywordButton.setText(_translate("HSIWebScraper", "Remove selected keyword"))
        self.newKeywordLabel.setText(_translate("HSIWebScraper", " Enter new keyword:"))
        self.newSetLabel.setText(_translate("HSIWebScraper", "Enter new set name:"))
        self.addSetButton.setText(_translate("HSIWebScraper", "Add set"))
        self.removeSetButton.setText(_translate("HSIWebScraper", "Remove selected set"))
        self.newSetLabel_2.setText(_translate("HSIWebScraper", "Select keywords from list on the left."))
        self.label_2.setText(_translate("HSIWebScraper", "Warning: Remove only one keyword at a time."))
        self.label_4.setText(_translate("HSIWebScraper", "Edit keywords and sets for scraper."))
        self.label_7.setText(_translate("HSIWebScraper", "NetSpider v1.0.0"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.EditKeywords), _translate("HSIWebScraper", "Edit Keywords"))


# ---------------------------- MainWindow - GUI Logic ----------------------------
'''WARNING: To make changes to UI do NOT edit Scraper.py, instead make changes to UI using Qt Creator.
Then run the following command to convert the .ui file to .py:
pyuic6 Scraper.ui -o Scraper.py
OR
python -m PyQt6.uic.pyuic -o Scraper.py -x Scraper.ui

'''


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_HSIWebScraper()
        self.ui.setupUi(self)
        self.keywords_instance = Keywords()
        self.facade = Facade()

        self.central_widget = self.ui.tabWidget
        self.setCentralWidget(self.ui.tabWidget)

        # attributes used to handle events
        self.website_selection = ''
        self.include_payment_method = False
        self.inclusive_search = False
        self.search_text = ''
        self.keywords_selected = set()
        self.keys_to_add_to_new_set = []
        self.manual_keyword_selection = set()
        self.set_keyword_selection = set()
        self.locations = []
        self.location = ''
        self.keywords = ''
        self.keyword_sets = ''

        self.setStyleSheet(qdarkstyle.load_stylesheet('pyqt6'))

        ''' Bind GUI components to functions: '''
        # bind websiteSelectionDropdown to website_selection_dropdown function
        self.ui.websiteSelectionDropdown.currentIndexChanged.connect(self.website_selection_dropdown)

        # disable button until website is selected
        self.ui.searchButton.setEnabled(False)
        # bind searchButton to search_button_clicked function
        self.ui.searchButton.clicked.connect(self.search_button_clicked)

        # bind paymentMethodCheckBox to payment_method_check_box function
        self.ui.paymentMethodcheckBox.stateChanged.connect(self.payment_method_check_box)

        # bind selectAllKeywordscheckBox to select_all_keywords_check_box function
        self.ui.selectAllKeywordscheckBox.stateChanged.connect(self.select_all_keywords_check_box)

        # bind searchTextBox to search_text_box function
        self.ui.searchTextBox.textChanged.connect(self.search_text_box)

        # bind keywordlistWidget to keyword_list_widget function
        self.ui.keywordlistWidget.itemClicked.connect(self.keyword_list_widget)

        # bind keywordInclusivecheckBox to keyword_inclusive_check_box function
        self.ui.keywordInclusivecheckBox.stateChanged.connect(self.keyword_inclusive_check_box)

        # bind setSelectionDropdown to set_selection_dropdown function
        self.ui.setSelectionDropdown.currentIndexChanged.connect(self.set_selection_dropdown)

        # bind addKeywordButton to add_keyword_button_clicked function
        self.ui.addKeywordButton.clicked.connect(self.add_keyword_button_clicked)

        # bind removeKeywordButton to remove_keyword_button_clicked function
        self.ui.removeKeywordButton.clicked.connect(self.remove_keyword_button_clicked)

        # bind addSetButton to add_set_button_clicked function
        self.ui.addSetButton.clicked.connect(self.add_set_button_clicked)

        # bind removeSetButton to remove_set_button_clicked function
        self.ui.removeSetButton.clicked.connect(self.remove_set_button_clicked)

        # bind locationTextBox to location_text_box function
        self.ui.setlocationDropdown.currentIndexChanged.connect(self.set_location)

        # bind setFileSelectionButton to set_file_selection_button_clicked function
        self.keyword_sets_file_path = ''
        self.ui.setFileSelectionButton.clicked.connect(self.set_file_selection_button_clicked)

        # bind keywordfileSelectionButton to keyword_file_selection_button_clicked function
        self.keyword_file_path = ''
        self.ui.keywordfileSelectionButton.clicked.connect(self.keyword_file_selection_button_clicked)

        # bind storagePathSelectionButton to storage_path_selection_button_clicked function
        self.file_storage_path = ''
        self.ui.storagePathSelectionButton.clicked.connect(self.storage_path_selection_button_clicked)
        # self.keywords_instance.set_file_storage_path(self.file_storage_path)

        from PyQt6.QtWidgets import QComboBox
        self.ui.setList.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # disable QtabWidget indices 1 and 2 until file paths are selected
        self.ui.tabWidget.setTabEnabled(1, True)
        self.ui.tabWidget.setTabEnabled(2, True)

    ''' Functions used to handle events: '''

    def enable_tabs(self):
        if self.keyword_file_path != '' and self.keyword_sets_file_path != '' and self.file_storage_path != '':
            self.ui.tabWidget.setTabEnabled(1, True)
            self.ui.tabWidget.setTabEnabled(2, True)
            self.ui.tabWidget.setCurrentIndex(1)

    def storage_path_selection_button_clicked(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.Directory)
        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            save_path = file_dialog.selectedFiles()[0]

            QMessageBox.information(self, "Success", f"Selected path: {save_path}")
            self.file_storage_path = save_path
            self.enable_tabs()

            self.ui.storagePathOutput.setText(self.file_storage_path)
            self.ui.storagePathProgressBar.setValue(100)

            self.facade.set_storage_path(self.file_storage_path)

    def keyword_file_selection_button_clicked(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Text files (*.txt)")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            file_path = file_dialog.selectedFiles()[0]
            if 'keywords.txt' in file_path:
                self.keyword_file_path = file_path
                self.enable_tabs()
                self.ui.keywordFilePathOutput.setText(self.keyword_file_path)
                self.ui.keywordFileProgressBar.setValue(100)

                self.keywords_instance.set_keywords_path(self.keyword_file_path)
                self.keywords = self.keywords_instance.get_keywords()
                self.initialize_keywords(self.keywords)
            else:
                QMessageBox.warning(self, "Error", "Please select 'keywords.txt'.")

    def set_file_selection_button_clicked(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Text files (*.txt)")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            file_path = file_dialog.selectedFiles()[0]
            if 'keyword_sets.txt' in file_path:
                self.keyword_sets_file_path = file_path
                self.enable_tabs()

                self.ui.keywordSetsPathOutput.setText(self.keyword_sets_file_path)
                self.ui.keywordSetsProgressBar.setValue(100)

                self.keywords_instance.set_keywords_sets_path(self.keyword_sets_file_path)
                self.keyword_sets = self.keywords_instance.get_set()
                self.initialize_keyword_sets(self.keyword_sets)
            else:
                QMessageBox.warning(self, "Error", "Please select 'keyword_sets.txt'.")

    # popup to confirm set removal
    @staticmethod
    def remove_set_popup_window(set_to_remove):
        popup = QtWidgets.QMessageBox()

        popup.setWindowTitle("Confirm Set Removal")
        popup.setText(f"Are you sure you want to remove {set_to_remove} from the list of sets?")
        popup.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)

        if popup.exec() == QtWidgets.QMessageBox.StandardButton.Yes:
            return True
        else:
            return False

    # remove set when button is clicked
    def remove_set_button_clicked(self):
        # get name of set to remove
        if self.ui.setList.currentItem() is not None:
            set_to_remove = self.ui.setList.currentItem().text()
        else:
            return

        confirmation = self.remove_set_popup_window(set_to_remove)
        if not confirmation:
            return

        # remove set from keyword_sets
        self.keywords_instance.remove_set(set_to_remove)

        # remove set from GUI
        self.ui.setList.takeItem(self.ui.setList.currentRow())

        # update list of sets
        self.ui.setSelectionDropdown.clear()
        self.ui.setSelectionDropdown.addItem('')
        self.keyword_sets = self.keywords_instance.get_set()
        self.ui.setSelectionDropdown.addItems(self.keyword_sets)

    # set location based on selection from the dropdown
    def set_location(self):
        self.location = self.ui.setlocationDropdown.currentText()

        if self.website_selection == 'eros':
            self.facade.set_eros_city(self.location)

        if self.website_selection == 'escortalligator':
            self.facade.set_escortalligator_city(self.location)

        if self.website_selection == 'yesbackpage':
            self.facade.set_yesbackpage_city(self.location)

        if self.website_selection == 'megapersonals':
            self.facade.set_megapersonals_city(self.location)

        if self.website_selection == 'skipthegames':
            self.facade.set_skipthegames_city(self.location)

    # initialize locations based on website that is selected
    def initialize_location_dropdown(self):
        self.ui.setlocationDropdown.clear()
        for location in self.locations:
            self.ui.setlocationDropdown.addItem(location)

    # add new set when button is clicked
    def add_set_button_clicked(self):
        # get name of new set
        if self.ui.newSetTextBox.text() != '':
            new_set_name = self.ui.newSetTextBox.text()
        else:
            return

        # get text from list
        for item in self.ui.keywordList.selectedItems():
            self.keys_to_add_to_new_set.append(item.text())

        # call create_set function from keywords class
        self.keywords_instance.create_set(new_set_name, self.keys_to_add_to_new_set)

        # update list of sets
        self.ui.setList.addItem(new_set_name)

        # make self.keys_to_add_to_new_set of an empty list
        self.keys_to_add_to_new_set = []

        # add new set to setSelectionDropdown
        self.ui.setSelectionDropdown.addItem(new_set_name)

        # clear new set text box
        self.ui.newSetTextBox.clear()

    # popup to confirm keyword removal
    @staticmethod
    def remove_keyword_popup_window(keyword_to_remove):
        popup = QtWidgets.QMessageBox()
        popup.setWindowTitle("Confirm Keyword Removal")
        popup.setText(f"Are you sure you want to remove {keyword_to_remove} from the list of keywords? \n\nWarning: "
                      f"{keyword_to_remove} will be removed from all sets.")
        font = popup.font()
        font.setBold(True)
        popup.setFont(font)
        popup.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)

        if popup.exec() == QtWidgets.QMessageBox.StandardButton.Yes:
            return True
        else:
            return False

    # TODO BUG - last item clicked on is deleted even if not selected
    # remove new keyword
    def remove_keyword_button_clicked(self):
        # find text of selected item
        if self.ui.keywordList.currentItem() is not None:
            keyword = self.ui.keywordList.currentItem().text()
        else:
            return

        # confirm keyword removal
        confirmation = self.remove_keyword_popup_window(keyword)

        if not confirmation:
            return

        self.remove_keyword(keyword)

        # loop through sets and remove keyword from each set
        for set_name in self.keyword_sets:
            if keyword in self.keywords_instance.get_set_values(set_name):
                self.keywords_instance.remove_keyword_from_set(keyword, set_name)

    # add new keyword
    def add_keyword_button_clicked(self):
        keyword = self.ui.newKeywordTextBox.text()

        if keyword != '':
            self.ui.keywordlistWidget.addItem(keyword)
            self.ui.keywordList.addItem(keyword)
            # add keyword to text file
            self.keywords_instance.add_keywords(keyword)

            # clear new keyword text box
            self.ui.newKeywordTextBox.clear()

    # initialize all keywords to scraper tab
    def initialize_keywords(self, keywords):
        for keyword in keywords:
            self.ui.keywordlistWidget.addItem(keyword)
            self.ui.keywordList.addItem(keyword)

    # initialize all keyword sets to GUI
    def initialize_keyword_sets(self, keyword_sets):
        for keyword_set in keyword_sets:
            self.ui.setSelectionDropdown.addItem(keyword_set)
            self.ui.setList.addItem(keyword_set)

    # remove keyword from keywordlistWidget
    def remove_keyword(self, keyword):
        # remove keyword from keywordlistWidget using keyword text
        for i in range(self.ui.keywordlistWidget.count()):
            if self.ui.keywordlistWidget.item(i).text() == keyword:
                self.ui.keywordlistWidget.takeItem(i)
                self.ui.keywordList.takeItem(i)

                # remove from text file
                self.keywords_instance.remove_keywords(keyword)
                break

    # handle list of keywords to be searched
    def keyword_list_widget(self):
        for item in self.ui.keywordlistWidget.selectedItems():
            self.manual_keyword_selection.add(item.text())

        # if a keyword is unselected, remove it from the set
        for i in range(self.ui.keywordlistWidget.count()):
            if not self.ui.keywordlistWidget.item(i).isSelected():
                self.manual_keyword_selection.discard(self.ui.keywordlistWidget.item(i).text())

    # handle dropdown menu for keyword sets
    def set_selection_dropdown(self):
        selected_set = self.ui.setSelectionDropdown.currentText()

        # if empty set, unselect all keywords
        if selected_set == '':
            for i in range(self.ui.keywordlistWidget.count()):
                if self.ui.keywordlistWidget.item(i).text() not in self.manual_keyword_selection:
                    self.ui.keywordlistWidget.item(i).setSelected(False)

            return

        # get keywords from selected set from keywords class
        keywords_of_selected_set = set(self.keywords_instance.get_set_values(selected_set))

        # select keywords_of_selected_set in keywordlistWidget
        for i in range(self.ui.keywordlistWidget.count()):
            if self.ui.keywordlistWidget.item(i).text() in keywords_of_selected_set:
                self.ui.keywordlistWidget.item(i).setSelected(True)

            elif self.ui.keywordlistWidget.item(i).text() not in self.manual_keyword_selection:
                self.ui.keywordlistWidget.item(i).setSelected(False)

        # unselect keywords that are not in selected set
        if not keywords_of_selected_set:
            for i in range(self.ui.keywordlistWidget.count()):
                if self.ui.keywordlistWidget.item(i).text() not in self.manual_keyword_selection:
                    self.ui.keywordlistWidget.item(i).setSelected(False)

    # scrape using text box input
    def search_text_box(self):
        self.search_text = self.ui.searchTextBox.text()

    def keyword_inclusive_check_box(self):
        if self.ui.keywordInclusivecheckBox.isChecked():
            self.inclusive_search = True
        else:
            self.inclusive_search = False

    # if checked, select all items in list widget
    def select_all_keywords_check_box(self):
        if self.ui.selectAllKeywordscheckBox.isChecked():
            self.ui.selectAllKeywordscheckBox.setEnabled(True)
            # select all items in list widget
            for i in range(self.ui.keywordlistWidget.count()):
                self.ui.keywordlistWidget.item(i).setSelected(True)
                self.keywords_selected.add(self.ui.keywordlistWidget.item(i).text())
        else:
            self.ui.selectAllKeywordscheckBox.setEnabled(False)
            self.keywords_selected = set()
            # deselect all items in list widget
            for i in range(self.ui.keywordlistWidget.count()):
                self.ui.keywordlistWidget.item(i).setSelected(False)

        # enable checkbox after it's unchecked
        self.ui.selectAllKeywordscheckBox.setEnabled(True)

    def payment_method_check_box(self):
        if self.ui.paymentMethodcheckBox.isChecked():
            self.ui.paymentMethodcheckBox.setEnabled(True)
            self.include_payment_method = True
        else:
            self.ui.paymentMethodcheckBox.setEnabled(False)
            self.include_payment_method = False

        # enable checkbox after it's unchecked
        self.ui.paymentMethodcheckBox.setEnabled(True)

    # handle dropdown menu for payment method
    def website_selection_dropdown(self):

        self.website_selection = self.ui.websiteSelectionDropdown.currentText()

        if self.website_selection != '':
            self.ui.searchButton.setEnabled(True)
        else:
            self.ui.searchButton.setEnabled(False)
            self.ui.setlocationDropdown.clear()

        if self.website_selection == 'eros':
            self.locations = self.facade.get_eros_cities()
            self.set_location()
            self.initialize_location_dropdown()

        if self.website_selection == 'escortalligator':
            self.locations = self.facade.get_escortalligator_cities()
            self.set_location()
            self.initialize_location_dropdown()

        if self.website_selection == 'yesbackpage':
            self.locations = self.facade.get_yesbackpage_cities()
            self.set_location()
            self.initialize_location_dropdown()

        if self.website_selection == 'megapersonals':
            self.locations = self.facade.get_megapersonals_cities()
            self.set_location()
            self.initialize_location_dropdown()

        if self.website_selection == 'skipthegames':
            self.locations = self.facade.get_skipthegames_cities()
            self.set_location()
            self.initialize_location_dropdown()

    # TODO - pop up when search button is clicked - show progress bar, status? & cancel button
    @staticmethod
    def search_popup_window(website_selection):
        popup = QtWidgets.QMessageBox()
        popup.setWindowTitle("Scraping in Progress")
        popup.setText(f"Scraping {website_selection} in progress...")
        popup.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Cancel)

        if popup.exec() == QtWidgets.QMessageBox.StandardButton.Cancel:
            popup.close()

    # scrape website selected when search button is clicked
    def search_button_clicked(self):
        # success/fail message box
        parent = QWidget()
        parent_width = parent.frameGeometry().width()
        parent_height = parent.frameGeometry().height()
        screen_width = QApplication.primaryScreen().availableGeometry().width()
        screen_height = QApplication.primaryScreen().availableGeometry().height()
        parent.move((screen_width - parent_width) // 2, (screen_height - parent_height) // 2)

        self.keywords_selected = set()

        # add input text to self.keywords_selected set

        # find keywords selected in keyword list widget
        for i in range(self.ui.keywordlistWidget.count()):
            if self.ui.keywordlistWidget.item(i).isSelected():
                self.keywords_selected.add(self.ui.keywordlistWidget.item(i).text())

        if self.search_text:
            self.keywords_selected.add(self.search_text)

        if self.website_selection == 'escortalligator':
            try:
                if self.inclusive_search:
                    self.facade.set_escortalligator_join_keywords()
                self.facade.initialize_escortalligator_scraper(self.keywords_selected)
                QMessageBox.information(parent, "Success", "Scrape completed successfully.")
            except:
                QMessageBox.critical(parent, "Error", "An error occurred: Scrape failed.")
            time.sleep(2)

        if self.website_selection == 'megapersonals':
            try:
                if self.inclusive_search:
                    self.facade.set_megapersonals_join_keywords()
                self.facade.initialize_megapersonals_scraper(self.keywords_selected)
                QMessageBox.information(parent, "Success", "Scrape completed successfully.")
            except:
                QMessageBox.critical(parent, "Error", "An error occurred: Scrape failed.")
            time.sleep(2)

        if self.website_selection == 'skipthegames':
            try:
                if self.inclusive_search:
                    self.facade.set_skipthegames_join_keywords()
                self.facade.initialize_skipthegames_scraper(self.keywords_selected)
                QMessageBox.information(parent, "Success", "Scrape completed successfully.")
            except:
                QMessageBox.critical(parent, "Error", "An error occurred: Scrape failed.")
            time.sleep(2)

        if self.website_selection == 'yesbackpage':
            try:
                if self.inclusive_search:
                    self.facade.set_yesbackpage_join_keywords()
                self.facade.initialize_yesbackpage_scraper(self.keywords_selected)
                QMessageBox.information(parent, "Success", "Scrape completed successfully.")
            except:
                QMessageBox.critical(parent, "Error", "An error occurred: Scrape failed.")
            time.sleep(2)

        if self.website_selection == 'eros':
            try:
                # self.run_threads(self.search_popup_window(self.website_selection),
                #                  self.facade.initialize_eros_scraper(self.keywords_selected))
                if self.inclusive_search:
                    self.facade.set_eros_join_keywords()
                self.facade.initialize_eros_scraper(self.keywords_selected)
                QMessageBox.information(parent, "Success", "Scrape completed successfully.")
            except:
                QMessageBox.critical(parent, "Error", "An error occurred: Scrape failed.")
            time.sleep(2)

        self.ui.keywordInclusivecheckBox.setChecked(False)

    # TODO - function two run threads simultaneously
    # function to run two threads at once
    # @staticmethod
    # def run_threads(function1, function2):
    #     thread1 = threading.Thread(target=function1)
    #     thread2 = threading.Thread(target=function2)
    #     thread1.start()
    #     thread2.start()
    #     thread2.join()


# ---------------------------- GUI Main ----------------------------

if __name__ == "__main__":
    app = QApplication([])
    app.setWindowIcon(QtGui.QIcon(os.path.join(basedir, "hsi.ico")))
    window = MainWindow()
    window.show()
    app.exec()
