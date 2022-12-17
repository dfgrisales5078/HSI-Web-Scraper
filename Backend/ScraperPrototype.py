from abc import ABC, abstractmethod
from Backend.Keywords import Keywords


class ScraperPrototype(ABC):
    def __init__(self, driver, location, join, payment, url, text_search):
        self.driver = driver
        self.location = location
        self.keywords = Keywords()
        self.join = join
        self.payment = payment
        self.url = url
        self.text_search = text_search

    @abstractmethod
    def initialize(self):
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
    def get_data(self):
        pass

    @abstractmethod
    def capture_screenshot(self):
        pass

    @abstractmethod
    def read_keywords(self):
        pass