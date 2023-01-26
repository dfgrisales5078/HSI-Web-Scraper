from Backend.DataPrototype import DataPrototype
from Backend.EscortalligatorScraper import EscortalligatorScraper
from Backend.MegapersonalsScraper import MegapersonalsScraper
from Backend.SkipthegamesScraper import SkipthegamesScraper
from Backend.YesbackpageScraper import YesbackpageScraper


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

    def format_data(self, data):
        pass
