import time
from selenium import webdriver
# from selenium.webdriver.chrome.options import Options as ChromeOptions
import logging
from selenium.webdriver.common.by import By
import pandas as pd

# LOG_FILE = 'listings_results.log'
# logging.basicConfig(level=logging.INFO,
#                     datefmt="%m/%d/%Y %H:%M:%S", filename=LOG_FILE)


class TestScraper:
    def __init__(self):
        self.driver = None
        self.location = 'fortmyers'
        self.keywords = ['cash', 'Exotic']
        self.join = ''
        self.payment = ['cash', 'cashapp', 'venmo']
        self.url = f'https://escortalligator.com.listcrawler.eu/brief/escorts/usa/florida/{self.location}/1'
        self.text_search = ''

        # lists to store data and then send to csv file
        self.phone_number = []
        self.description = []
        self.location_and_age = []
        self.links = []

    def initialize(self):
        # options = ChromeOptions()
        # options.headless = False
        self.driver = webdriver.Firefox()
        self.open_webpage()

        links = self.get_links()
        self.get_data(links)
        self.close_webpage()
        self.format_data_to_csv()

        # self.check_post_for_keywords(self.get_data())
        # time.sleep(3)
        # self.capture_screenshot()
        # time.sleep(2)

    def get_links(self):
        posts = self.driver.find_elements(
            By.CSS_SELECTOR, '#list [href]')
        links = [post.get_attribute('href') for post in posts]

        print(links[::3])
        return links[::3]

    def open_webpage(self) -> None:
        self.driver.implicitly_wait(10)
        self.driver.get(self.url)
        assert "Page not found" not in self.driver.page_source

        # click on terms btn
        btn = self.driver.find_element(
            By.CLASS_NAME, 'button')
        btn.click()

        time.sleep(2)
        # click on terms btn
        btn1 = self.driver.find_element(
            By.CLASS_NAME, 'footer')
        btn1.click()

    def close_webpage(self) -> None:
        self.driver.close()

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

            description = self.driver.find_element(
                By.CLASS_NAME, 'viewpostbody')
            print(description.text)

            # append description to list
            self.description.append(description.text)

            phone_number = self.driver.find_element(
                By.CLASS_NAME, 'userInfoContainer')
            print(phone_number.text)

            # append phone number to list
            self.phone_number.append(phone_number.text)

            location_and_age = self.driver.find_element(
                By.CLASS_NAME, 'viewpostlocationIconBabylon')
            print(location_and_age.text)

            # append location and age to list
            self.location_and_age.append(location_and_age.text)

            # info = description.text + phone_number.text + location_and_age.text

            # for line in info:
            #     if 'call' in line.lower():
            #         print(line)
            #         print('keyword found')

            screenshot_name = str(counter) + ".png"
            self.capture_screenshot(screenshot_name)
            counter += 1

            if counter > 2:
                break
            time.sleep(3)

    def format_data_to_csv(self):
        titled_columns = {
            'Phone-Number': self.phone_number,
            'Link': self.links,
            'Location/Age': self.location_and_age,
            'Description': self.description
        }

        data = pd.DataFrame(titled_columns)
        data.to_csv('escort_alligator_01-20-23.csv', index=False, sep="\t")

    def check_post_for_keywords(self, data):
        for keyword in self.keywords:
            if keyword in data[0] or keyword in data[1]:
                logging.info(data)
            break

    def capture_screenshot(self, screenshot_name):
        self.driver.save_screenshot(f'screenshots/{screenshot_name}')

    def read_keywords(self) -> str:
        return ' '.join(self.keywords)


if __name__ == "__main__":
    scraper = TestScraper()
    scraper.initialize()
