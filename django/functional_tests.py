""" /functional_test.py
    integration testing for overall system

    this mainly tests hypermedia behaviors for user (front-end)
"""
import os
import re
import pytest
from urllib.parse import urljoin, urlparse
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


@pytest.fixture(scope='session')
def browser():
    browser = webdriver.Chrome(os.environ.get('SELENIUM_WEBDRIVER_CHROME', 'C:/Tools/chromedriver.exe'))
    browser.implicitly_wait(3)
    yield browser
    browser.quit()


@pytest.mark.functional
class BrowserTestHelper:
    """
    helper class for functional tests with selenium webdriver
    """
    fixtures_to_use = ('browser', )
    server_url = 'http://localhost:80'

    @pytest.fixture(autouse=True)
    def _auto_inject_fixtures(self, request):
        """
        this injects fixtures defined in 'fixtures_to_use' attribute into class instance attribute
        """
        names = self.fixtures_to_use
        for name in names:
            setattr(self, name, request.getfixturevalue(name))

    def get(self, url):
        return self.browser.get(urljoin(self.server_url, url))


# ==================================================================================================================== #


class IndexPageTest(BrowserTestHelper):
    """
    tests for /, application home page
    """
    page_url = '/'

    def test_browser_ui_includes_menu(self):
        self.get(self.page_url)

    def test_user_enjoy_image_carousel(self):
        # user get to the main page and find 'Take a Look' in title
        self.get(self.page_url)
        assert 'Take a Look' in self.browser.title

        # user find image carousel
        try:
            carousel = self.browser.find_element_by_id('recent-submits')
        except NoSuchElementException:
            assert False, 'Carousel is not found'

        # when user clicks image, then will be moved to its page (new state)
        pattern = re.compile('^/history/*[0-9]/$')  # item pattern is expected to be integer!
        carousel.click()
        assert pattern.match(urlparse(self.browser.current_url).path) is not None


class HistoryPageTest(BrowserTestHelper):
    """
    tests for /history, user submitted image list page
    """
    page_url = '/history/'

    def test_user_browse_images(self):
        # user get to history page to look around some kitty images, for time killing or whatever
        self.get(self.page_url)
        assert 'Take a Look' in self.browser.title

        #

        assert False, 'Test is not done'


class PredictionPageTest(BrowserTestHelper):
    """
    tests for /history/:id/, user submitted image detail with specific informations about it
    """
    @staticmethod
    def page_url(item):  # /history/:item/
        return f'/history/{item}/'

    def test_(self):
        assert False, 'Test is never written'
