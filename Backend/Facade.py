from Backend.Scrapers.EscortalligatorScraper import EscortalligatorScraper
from Backend.Scrapers.MegapersonalsScraper import MegapersonalsScraper
from Backend.Scrapers.SkipthegamesScraper import SkipthegamesScraper
from Backend.Scrapers.YesbackpageScraper import YesbackpageScraper
from Backend.Scrapers.ErosScraper import ErosScraper

class Facade:
    def __init__(self):
        pass
        # self.data = DataPrototype()

    @staticmethod
    def initialize_escortalligator_scraper():
        escortalligator = EscortalligatorScraper()
        escortalligator.initialize()

    @staticmethod
    def initialize_megapersonals_scraper():
        megapersonals = MegapersonalsScraper()
        megapersonals.initialize()

    @staticmethod
    def initialize_skipthegames_scraper():
        skipthegames = SkipthegamesScraper()
        skipthegames.initialize()

    @staticmethod
    def initialize_yesbackpage_scraper():
        yesbackpage = YesbackpageScraper()
        yesbackpage.initialize()

    @staticmethod
    def initialize_eros_scraper():
        eros = ErosScraper()
        eros.initialize()

    def format_data(self, data):
        pass
