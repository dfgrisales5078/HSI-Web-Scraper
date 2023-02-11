from Backend.Scrapers.EscortalligatorScraper import EscortalligatorScraper
from Backend.Scrapers.MegapersonalsScraper import MegapersonalsScraper
from Backend.Scrapers.SkipthegamesScraper import SkipthegamesScraper
from Backend.Scrapers.YesbackpageScraper import YesbackpageScraper
from Backend.Scrapers.ErosScraper import ErosScraper

class Facade:
    def __init__(self):
        # self.megapersonals = None
        self.eros = None
        self.escortalligator = None
        self.yesbackpage = None

    def initialize_escortalligator_scraper(self):
        self.escortalligator.initialize()

    def set_escortalligator_city(self, city):
        self.escortalligator.set_city(city)

    def get_escortalligator_cities(self):
        self.escortalligator = EscortalligatorScraper()
        return self.escortalligator.get_cities()

    @staticmethod
    def initialize_megapersonals_scraper():
        megapersonals = MegapersonalsScraper()
        megapersonals.initialize()

    # def set_megapersonals_city(self, city):
    #     self.megapersonals.set_city(city)
    #
    # def get_megapersonals_cities(self):
    #     self.megapersonals = MegapersonalsScraper()
    #     return self.megapersonals.get_cities()

    @staticmethod
    def initialize_skipthegames_scraper():
        skipthegames = SkipthegamesScraper()
        skipthegames.initialize()

    def initialize_yesbackpage_scraper(self):
        self.yesbackpage.initialize()

    def set_yesbackpage_city(self, city):
        self.yesbackpage.set_city(city)

    def get_yesbackpage_cities(self):
        self.yesbackpage = YesbackpageScraper()
        return self.yesbackpage.get_cities()

    def initialize_eros_scraper(self):
        self.eros.initialize()

    def set_eros_city(self, city):
        self.eros.set_city(city)

    def get_eros_cities(self):
        self.eros = ErosScraper()
        return self.eros.get_cities()

    def format_data(self, data):
        pass
