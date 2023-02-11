from Backend.Scrapers.EscortalligatorScraper import EscortalligatorScraper
from Backend.Scrapers.MegapersonalsScraper import MegapersonalsScraper
from Backend.Scrapers.SkipthegamesScraper import SkipthegamesScraper
from Backend.Scrapers.YesbackpageScraper import YesbackpageScraper
from Backend.Scrapers.ErosScraper import ErosScraper


class Facade:
    def __init__(self):
        pass
        self.eros = ErosScraper()
        self.escortalligator = EscortalligatorScraper()  # BUG: instead of None
        self.yesbackpage = YesbackpageScraper()
        self.megapersonals = MegapersonalsScraper()
        self.skipthegames = SkipthegamesScraper()

    def initialize_escortalligator_scraper(self, keywords):
        self.escortalligator.initialize(keywords)

    def set_escortalligator_city(self, city):
        self.escortalligator.set_city(city)

    def get_escortalligator_cities(self):
        return self.escortalligator.get_cities()

    @staticmethod
    def initialize_megapersonals_scraper(self, keywords):
        self.megapersonals.initialize(keywords)

    @staticmethod
    def initialize_skipthegames_scraper(self, keywords):
        self.skipthegames.initialize(keywords)

    def initialize_yesbackpage_scraper(self, keywords):
        self.yesbackpage.initialize(keywords)

    def set_yesbackpage_city(self, city):
        self.yesbackpage.set_city(city)

    def get_yesbackpage_cities(self):
        return self.yesbackpage.get_cities()

    def initialize_eros_scraper(self, keywords):
        self.eros.initialize(keywords)

    def set_eros_city(self, city):
        self.eros.set_city(city)

    def get_eros_cities(self):
        return self.eros.get_cities()

    def format_data(self, data):
        pass
