import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
import logging


LOG_FILE = 'listings_results.log'
logging.basicConfig(level=logging.INFO,
                    datefmt="%m/%d/%Y %H:%M:%S", filename=LOG_FILE)


class TestScraper:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.location = 'fort-myers'
        self.keywords = ['cash', 'Exotic']
        self.join = ''
        self.payment = ['cash', 'cashapp', 'venmo']
        self.url = 'https://skipthegames.com/posts/'
        self.text_search = ''

    def initialize(self):
        self.open_webpage()
        time.sleep(3)
        self.check_post_for_keywords(self.get_data())
        time.sleep(3)
        self.capture_screenshot()
        self.close_webpage()

    def open_webpage(self) -> None:
        self.driver.get(self.get_formatted_url())
        assert "Page not found" not in self.driver.page_source

    def close_webpage(self) -> None:
        self.driver.close()

    def get_formatted_url(self) -> str:
        return f'https://skipthegames.com/posts/{self.location}/"'

    def get_data(self) -> list:
        self.driver.find_element(
            By.XPATH, '// *[ @ id = "radio_clsfd_display_mode_single"]').click()
        time.sleep(2)

        first_post = self.driver.find_element(
            By.XPATH, '//*[@id="single_view"]/table/tbody/tr[1]/td[1]/a')
        first_post.click()
        time.sleep(2)

        table_info = self.driver.find_element(
            By.XPATH, '/html/body/div[7]/div/div[2]/div/table').text
        description_div = self.driver.find_element(
            By.XPATH, '/html/body/div[7]/div/div[2]/div/div[1]/div').text
        time.sleep(2)

        print([table_info, description_div])
        print(len([table_info, description_div]))
        return [table_info, description_div]

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
