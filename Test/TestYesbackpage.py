import pytest
from selenium import webdriver
from Backend.Scraper.YesbackpageScraper import YesbackpageScraper

class TestYesbackpage:
    @pytest.fixture
    def scraper(self):
        scraper = YesbackpageScraper()
        scraper.driver = webdriver.Firefox()
        return scraper

    def test_get_cities(scraper):
        cities = scraper.get_cities()
        assert len(cities) == 21
        assert 'florida' in cities

    def test_set_city(scraper):
        scraper.set_city('florida')
        assert scraper.city == 'florida'

    def test_set_join_keywords(scraper):
        scraper.set_join_keywords()
        assert scraper.join_keywords == True

    def test_set_only_posts_with_payment_methods(scraper):
        scraper.set_only_posts_with_payment_methods()
        assert scraper.only_posts_with_payment_methods == True

    def test_get_formatted_url(scraper):
        scraper.set_city('florida')
        scraper.get_formatted_url()
        assert scraper.url == 'https://www.yesbackpage.com/-10/posts/8-Adult/'

    def test_open_webpage(scraper):
        scraper.set_city('florida')
        scraper.get_formatted_url()
        scraper.open_webpage()
        assert "Page not found" not in scraper.driver.page_source

    def test_close_webpage(scraper):
        scraper.set_city('florida')
        scraper.get_formatted_url()
        scraper.open_webpage()
        scraper.close_webpage()
        with pytest.raises(Exception):
            scraper.driver.title

    def test_get_links(scraper):
        scraper.set_city('florida')
        scraper.get_formatted_url()
        scraper.open_webpage()
        links = scraper.get_links()
        scraper.close_webpage()
        assert len(links) > 0

