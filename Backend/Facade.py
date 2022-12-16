from Backend.DataPrototype import DataPrototype
from Backend.ScraperPrototype import ScraperPrototype


class Facade:
    def __init__(self):
        self.data = DataPrototype()
        self.scraper = ScraperPrototype()

    def initialize_scraper(self):
        pass

    def format_data(self):
        pass