from ScraperPrototype import ScraperPrototype
from selenium.webdriver.common.by import By


class FacebookScraper(ScraperPrototype):

    def __init__(self, driver, location, join, payment, url, text_search):
        super().__init__(driver, location, join, payment, url, text_search)

    def initialize(self):
        pass

    def open_webpage(self):
        pass

    def close_webpage(self):
        pass

    def get_formatted_url(self):
        pass

    def get_data(self):
        pass

    def capture_screenshot(self):
        pass

    def read_keywords(self):
        pass