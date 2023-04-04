from Backend.Facade import Facade

class TestFacade:
    def setup_method(self):
        self.facade = Facade()

    def test_initialize_escortalligator_scraper(self):
        keywords = ['escort', 'massage']
        self.facade.initialize_escortalligator_scraper(keywords)
        assert self.facade.escortalligator.scraper is not None

    def test_set_escortalligator_city(self):
        city = 'New York'
        self.facade.set_escortalligator_city(city)
        assert self.facade.escortalligator.city == city

    def test_set_escortalligator_join_keywords(self):
        self.facade.set_escortalligator_join_keywords()
        assert self.facade.escortalligator.join_keywords == True

    def test_get_escortalligator_cities(self):
        cities = self.facade.get_escortalligator_cities()
        assert isinstance(cities, list)

    def test_set_escortalligator_only_posts_with_payment_methods(self):
        self.facade.set_escortalligator_only_posts_with_payment_methods()
        assert self.facade.escortalligator.only_posts_with_payment_methods == True

    def test_initialize_megapersonals_scraper(self):
        keywords = ['escort', 'massage']
        self.facade.initialize_megapersonals_scraper(keywords)
        assert self.facade.megapersonals.scraper is not None

    def test_set_megapersonals_city(self):
        city = 'Los Angeles'
        self.facade.set_megapersonals_city(city)
        assert self.facade.megapersonals.city == city

    def test_set_megapersonals_join_keywords(self):
        self.facade.set_megapersonals_join_keywords()
        assert self.facade.megapersonals.join_keywords == True

    def test_get_megapersonals_cities(self):
        cities = self.facade.get_megapersonals_cities()
        assert isinstance(cities, list)

    def test_set_megapersonal_only_posts_with_payment_methods(self):
        self.facade.set_megapersonal_only_posts_with_payment_methods()
        assert self.facade.megapersonals.only_posts_with_payment_methods == True
