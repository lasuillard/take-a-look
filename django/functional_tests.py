""" /functional_test.py
    integration testing for overall system

    this mainly tests hypermedia behaviors for user (front-end)

    points to think about:
    - for testing <a>, or link, will it be just appropriate?
    - vue/vuetify components are not directly accessible via id; better way for doing this?
"""
import os
import re
import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from test_helper import (
    BrowserTestHelper,
    check_url_pattern,
    find_element_by_css_selector, find_elements_by_css_selector
)


@pytest.fixture(scope='session')
def browser():
    browser = webdriver.Chrome(os.environ.get('SELENIUM_WEBDRIVER_CHROME', 'C:/Tools/chromedriver.exe'))
    browser.implicitly_wait(1)
    yield browser
    browser.quit()


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
        navbar = find_element_by_css_selector(self.browser, '#bottom-navbar')
        assert navbar is not None, 'Navigation bar is not found; did you forget?'

        # using 'navbar' instead of 'self.browser' to make sure that link is child of navbar
        for (selector, url_pattern) in [('#navbar-link-home', '^/$'),
                                        ('#navbar-link-history', '^/history$'),
                                        ('#navbar-link-model', '^/model$')]:
            link = find_element_by_css_selector(navbar, selector)
            href = link.get_attribute('href')
            assert check_url_pattern(href, url_pattern)

    def test_user_enjoy_image_carousel(self):
        # user find image carousel
        self.get(self.page_url)
        carousel = find_element_by_css_selector(self.browser, '#recent-submits')
        assert carousel is not None, 'Carousel is not visible'

        # when user clicks image, then will be moved to its page (new state)
        # the selenium tester decided to pick one what it see
        links = find_elements_by_css_selector(carousel, 'a')
        for link in links:
            assert check_url_pattern(link.get_attribute('href'), r'^/history/\d+$')

    def test_simple_descriptions_of_models_provided(self):
        # finally user arrived at our models's preview
        # it is some kind of drawer component, or accordion, or something like that
        self.get(self.page_url)
        preview = find_element_by_css_selector(self.browser, '#model-previews')
        assert preview is not None, 'Preview for models is not found'

        # our selenium tester will test all models in the container
        # then first collect all model ids
        models = [model.get_attribute('id')
                  for model
                  in find_elements_by_css_selector(preview, '.v-expansion-panel')]
        assert None not in models, 'All items in model preview must have id for identification'

        # click and check href one by one
        for eid in models:
            model = find_element_by_css_selector(self.browser, f'#{eid}')
            btn = find_element_by_css_selector(model, 'button')
            _ = btn.location_once_scrolled_into_view  # scroll to model
            btn.click()
            link = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a')))
            assert link is not None, \
                'No link in this model: {}; did you forget?'.format(model.get_attribute('id'))
            assert check_url_pattern(link.get_attribute('href'), r'^/model/\w+$')


class HistoryPageTest(BrowserTestHelper):
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
        container = find_element_by_css_selector(self.browser, '#image-container')
        assert container is not None

        # and pick first one, and it is linked to its detail page!
        assert False, 'Test is not done'


class HistoryDetailPageTest(BrowserTestHelper):
    """
    tests for /history/:id, user submitted image detail with specific informations about it
    """
    @staticmethod
    def page_url(item):  # /history/:item
        return f'/history/{item}'

    def test_(self):
        pass


class ModelPageTest(BrowserTestHelper):
    """
    tests for /model, list of machine learning models supported by server will be shown
    """
    page_url = '/model'

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
        return f'/model/{name}'

    def test_(self):
        pass
