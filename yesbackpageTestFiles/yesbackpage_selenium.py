import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import logging
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

LOG_FILE = 'listings_results.log'
logging.basicConfig(level=logging.INFO,
                    datefmt="%m/%d/%Y %H:%M:%S", filename=LOG_FILE)


class TestScraper:
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.location = 'fortmyers'
        self.keywords = ['cash', 'Exotic']
        self.join = ''
        self.payment = ['cash', 'cashapp', 'venmo']
        self.url = f'https://www.yesbackpage.com/68/posts/8-Adult/122-Female-Escorts'
        self.text_search = ''

    def initialize(self):
        self.open_webpage()
        links = self.get_links()
        self.get_data(links)

        # self.check_post_for_keywords(self.get_data())
        # time.sleep(3)
        # self.capture_screenshot()
        # self.close_webpage()
        # time.sleep(2)

    def open_webpage(self) -> None:
        # self.driver.implicitly_wait(10)
        self.driver.get(self.url)
        # assert "Page not found" not in self.driver.page_source

    def close_webpage(self) -> None:
        self.driver.close()

    def get_links(self):
        posts = self.driver.find_elements(
            By.CSS_SELECTOR, '#mainCellWrapper > div.mainBody > table [href]')
        links = [post.get_attribute('href') for post in posts]
        return links[2:]

    def get_data(self, links):
        counter = 0
        for link in links:
            counter += 1

            print(link)
            self.driver.implicitly_wait(10)
            self.driver.get(link)
            assert "Page not found" not in self.driver.page_source
            table = self.driver.find_element(
                By.XPATH, '//*[@id="mainCellWrapper"]/div[1]/table/tbody/tr[1]/td/div[1]/div/table')
            print(table.text)

            description = self.driver.find_element(
                By.XPATH, '//*[@id="mainCellWrapper"]/div[1]/table/tbody/tr[1]/td/table[2]/tbody/tr/td/div')
            print(description.text)
            print("\n")

            info = table.text + description.text

            for line in info:
                if 'call' in line.lower():
                    print(line)
                    print('keyword found')

            if counter > 6:
                break

    def check_post_for_keywords(self, data):
        for keyword in self.keywords:
            if keyword in data[0] or keyword in data[1]:
                logging.info(data)
            break

    def capture_screenshot(self):
        self.driver.save_screenshot("test_search.png")

    def read_keywords(self) -> str:
        return ' '.join(self.keywords)


if __name__ == "__main__":
    scraper = TestScraper()
    scraper.initialize()
