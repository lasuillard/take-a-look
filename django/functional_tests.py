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
    browser.implicitly_wait(1)
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

    @staticmethod
    def is_url_pattern_matches(url, pattern):
        """
        receive absolute or relative url, and 'path' part will be compared to regex pattern
        """
        if isinstance(pattern, str):
            p = re.compile(pattern)
        elif isinstance(pattern, re.Pattern):
            p = pattern
        else:
            raise TypeError('Expected type (str, re.Pattern) but received: {}'.format(type(pattern)))

        return p.match(urlparse(url).path) is not None

    def get(self, url):
        return self.browser.get(urljoin(self.server_url, url))

    def find_element_by_id(self, eid, default=None):
        try:
            element = self.browser.find_element_by_id(eid)
        except NoSuchElementException:
            return default
        else:
            return element


# ==================================================================================================================== #


class IndexPageTest(BrowserTestHelper):
    """
    tests for /, application home page
    self.get() is being used multiple times because some tests may contain state change(hyperlinks, especially href)
    """
    page_url = '/'

    def test_page_well_served(self):
        # user visit main page and find 'Take a Look' in title
        self.get(self.page_url)
        assert 'Take a Look' in self.browser.title

    def test_bottom_navigation_bar_works_well(self):
        # user look layouts, especially our simple & fancy bottom bar
        self.get(self.page_url)
        navbar = self.find_element_by_id('bottom-navbar')
        assert navbar is not None, 'Navigation bar is not found; did you forget?'

        # using 'navbar' instead of 'self.browser' to make sure that link is child of navbar
        # is navbar has index(home) link?
        link_to_home = navbar.find_element_by_id('navbar-link-home')
        assert self.is_url_pattern_matches(link_to_home.get_attribute('href'), '^/$')

        # is navbar has link to history?
        link_to_history = navbar.find_element_by_id('navbar-link-history')
        assert self.is_url_pattern_matches(link_to_history.get_attribute('href'), '^/history/$')

        # is navbar has link to model list?
        link_to_model = navbar.find_element_by_id('navbar-link-model')
        assert self.is_url_pattern_matches(link_to_model.get_attribute('href'), '^/model/$')

    def test_user_enjoy_image_carousel(self):
        # user find image carousel
        self.get(self.page_url)
        carousel = self.find_element_by_id('recent-submits')
        assert carousel is not None, 'Carousel is not visible'

        # when user clicks image, then will be moved to its page (new state)
        # the selenium tester decided to pick one what it see
        links = carousel.find_elements_by_tag_name('a')
        pattern = re.compile(r'^/history/\d+/$')
        for link in links:
            assert self.is_url_pattern_matches(link.get_attribute('href'), pattern)

    def test_simple_descriptions_of_models_provided(self):
        # finally user arrived at our models's preview
        # it is some kind of drawer component, or accordion, or something like that
        self.get(self.page_url)
        preview = self.browser.find_element_by_id('model-previews')
        assert preview is not None, 'Preview for models is not found'

        # web will introduce them to model's detail description page by clicking its link
        # and our tester will just pick first one
        try:
            model = preview.find_element_by_id('model-1')
        except NoSuchElementException:
            assert False, 'No models shown; is database or API alright?'

        model.click()  # open accordion or collapsed
        try:
            link = model.find_element_by_id('model-1-link')
        except NoSuchElementException:
            assert False, 'No link found for model content; may view template or test malformed'

        assert self.is_url_pattern_matches(link.get_attribute('href'), re.compile(r'^/model/\w+/$'))


class HistoryPageTest(BrowserTestHelper):
    """
    tests for /history/, user submitted image list page
    """
    page_url = '/history/'

    def test_user_browse_images(self):
        # user get to history page to look around some kitty images, for time killing or whatever
        self.get(self.page_url)
        assert 'Take a Look' in self.browser.title

        #

        assert False, 'Test is not done'


class HistoryDetailPageTest(BrowserTestHelper):
    """
    tests for /history/:id/, user submitted image detail with specific informations about it
    """
    @staticmethod
    def page_url(item):  # /history/:item/
        return f'/history/{item}/'

    def test_(self):
        pass


class ModelPageTest(BrowserTestHelper):
    """
    tests for /model/, list of machine learning models supported by server will be shown
    """
    page_url = '/model/'

    def test_page_well_served(self):
        self.get(self.page_url)
        assert 'Take a Look' in self.browser.title


class ModelDetailPageTest(BrowserTestHelper):
    """
    tests for /model/:name/, where detailed description of ML model provided
    it is likely to include some visualization components
    """
    @staticmethod
    def page_url(name):
        return f'/model/{name}/'

    def test_(self):
        pass
