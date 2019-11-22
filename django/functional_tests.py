""" /functional_test.py
    integration testing for overall system

    this mainly tests hypermedia behaviors for user (front-end)

    testing strategies:
    - locate
        - find elements by html id attribute
        - find vuetify components via html class, like: .v-expansion-panel-header
    - behavior
        - link test with attribute 'href'

    notes:
    - selenium.webdriver.support.ui.WebDriverWait
        - it takes webdriver as argument but i found that it is not necessarily be a selenium webdriver
          because its behaviors are like:

            while True:
              value = method(driver)
              if value:
                  return value
              else:
                  wait(short)

          so using selenium DOM element won't be a problem

"""
import os
import re
import time
from urllib.parse import urljoin
import pytest
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains as Action
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as Wait
from test_helper import (
    check_url_pattern,
    find_element, find_elements_all
)


@pytest.fixture(scope='session')
def browser():
    browser = webdriver.Chrome(os.environ.get('SELENIUM_WEBDRIVER_CHROME', 'C:/Tools/chromedriver.exe'))
    browser.implicitly_wait(1)
    yield browser
    browser.quit()


@pytest.mark.functional
class PageTestBase:
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


class IndexPageTest(PageTestBase):
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
        navbar = find_element(self.browser, '#bottom-navbar')
        assert navbar is not None, 'Navigation bar is not found; did you forget?'

        # using 'navbar' instead of 'self.browser' to make sure that link is child of navbar
        for (selector, url_pattern) in [('#navbar-link-home', '^/$'),
                                        ('#navbar-link-history', '^/history$'),
                                        ('#navbar-link-model', '^/model$')]:
            link = find_element(navbar, selector)
            href = link.get_attribute('href')
            assert check_url_pattern(href, url_pattern)

    def test_user_enjoy_image_carousel(self):
        # user find image carousel
        self.get(self.page_url)
        carousel = find_element(self.browser, '#recent-submits')
        assert carousel is not None, 'Carousel is not visible'

        # when user clicks image, then will be moved to its page (new state)
        # the selenium tester decided to pick one what it see
        links = find_elements_all(carousel, 'a')
        for link in links:
            assert check_url_pattern(link.get_attribute('href'), r'^/history/\d+$')

    def test_simple_descriptions_of_models_provided(self):
        # finally user arrived at our models's preview
        # it is some kind of drawer component, or accordion, or something like that
        self.get(self.page_url)
        preview = find_element(self.browser, '#model-previews')
        assert preview is not None, 'Preview for models is not found'

        # our selenium tester will test all models in the container
        # then first collect all model ids
        models = [model.get_attribute('id')
                  for model
                  in find_elements_all(preview, '.v-expansion-panel')]
        assert None not in models, 'All items in model preview must have id for identification'

        # click and check href one by one
        for eid in models:
            model = find_element(self.browser, f'#{eid}')
            header = find_element(model, '.v-expansion-panel-header')
            assert header is not None, 'No header for model to click: {}; component changed? '.format(eid)

            header.click()
            link = Wait(model, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.v-btn')))
            assert link is not None, 'No link in this model: {}; did you forget?'.format(eid)
            assert check_url_pattern(link.get_attribute('href'), r'^/model/\w+$')


class HistoryPageTest(PageTestBase):
    """
    tests for /history, user submitted image list page
    """
    page_url = '/history'

    def test_page_served_well(self):
        self.get(self.page_url)
        assert 'Take a Look' in self.browser.title

    def test_user_browse_images(self):
        # user get to history page to look around some kitty images, for time killing or whatever
        # and find the image container
        self.get(self.page_url)
        container = find_element(self.browser, '#image-container')
        assert container is not None

        # and pick first one, and it is linked to its detail page!
        assert False, 'Test is not done'


class HistoryDetailPageTest(PageTestBase):
    """
    tests for /history/:id, user submitted image detail with specific informations about it
    """
    @staticmethod
    def page_url(item):  # /history/:item
        return f'/history/{item}'

    def test_(self):
        pass


class ModelPageTest(PageTestBase):
    """
    tests for /model, list of machine learning models supported by server will be shown
    """
    page_url = '/model'

    def test_page_well_served(self):
        self.get(self.page_url)
        assert 'Take a Look' in self.browser.title


class ModelDetailPageTest(PageTestBase):
    """
    tests for /model/:name/, where detailed description of ML model provided
    it is likely to include some visualization components
    """
    @staticmethod
    def page_url(name):
        return f'/model/{name}'

    def test_(self):
        pass
