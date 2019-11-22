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

          so using selenium DOM element for argument 'driver' won't be a problem

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
    check_url_pattern,  # use compiled pattern in repeated tests
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

    @classmethod
    def setup_class(cls):
        for attr in ['page_url', 'pattern']:
            if not hasattr(cls, attr):
                raise AttributeError('Required attribute not found: {}'.format(attr))

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


class PageLayoutTestMixin(PageTestBase):

    def test_bottom_navigation_bar_works_well(self):
        # user look layouts, especially our simple & fancy bottom bar
        self.get(self.page_url() if callable(self.page_url) else self.page_url)
        navbar = find_element(self.browser, '#bottom-navbar')
        assert navbar is not None, 'Navigation bar is not found; did you forget?'

        # using 'navbar' instead of 'self.browser' to make sure that link is child of navbar
        for (selector, url_pattern) in [('#navbar-link-home', IndexPageTest.pattern),
                                        ('#navbar-link-history', HistoryPageTest.pattern),
                                        ('#navbar-link-model', ModelPageTest.pattern),
                                        ('#navbar-link-predict', PredictPageTest.pattern)]:
            link = find_element(navbar, selector)
            href = link.get_attribute('href')
            assert check_url_pattern(href, url_pattern)


class IndexPageTest(PageLayoutTestMixin):
    """
    tests for /, application home page
    self.get() is being used multiple times because some tests may contain state change(hyperlinks, especially href)
    """
    page_url = '/'
    pattern = re.compile(r'^/$')

    def test_page_well_served(self):
        # user visit main page and find 'Take a Look' in title
        self.get(self.page_url)
        assert 'Take a Look' in self.browser.title

    def test_user_enjoy_image_carousel(self):
        # user find image carousel
        self.get(self.page_url)
        carousel = find_element(self.browser, '#recent-submits')
        assert carousel is not None, 'Carousel is not visible'

        # when user clicks image, then will be moved to its page (new state)
        # the selenium tester decided to pick one what it see
        links = find_elements_all(carousel, 'a')
        for link in links:
            assert check_url_pattern(link.get_attribute('href'), HistoryDetailPageTest.pattern)

    def test_simple_descriptions_of_models_provided(self):
        # finally user arrived at our models's preview
        # it is some kind of drawer component, or accordion, or something like that
        self.get(self.page_url)
        preview = find_element(self.browser, '#model-previews')
        assert preview is not None, 'Preview for models is not found'

        # our selenium tester will test all models in the container
        # model should be shown at least one
        models = find_elements_all(preview, '.v-expansion-panel')
        assert len(models) > 0

        # click model header to open and check links for its detail page
        for model in models:
            model_id = model.get_attribute('id')
            # find header
            header = find_element(model, '.v-expansion-panel-header')
            assert header is not None,\
                'No header for model to click; component changed? '.format(model_id)

            # open collapsed and check link
            header.click()
            link = Wait(model, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.v-btn')))
            assert link is not None, 'No link in this model: {}; did you forget?'.format(model_id)
            assert check_url_pattern(link.get_attribute('href'), ModelDetailPageTest.pattern)


class HistoryPageTest(PageLayoutTestMixin):
    """
    tests for /history, user submitted image list page
    """
    page_url = '/history'
    pattern = re.compile(r'^/history$')

    def test_page_served_well(self):
        self.get(self.page_url)
        assert 'Take a Look' in self.browser.title

    def test_user_browse_images(self):
        # user get to history page to look around some kitty images, for time killing or whatever
        # and find the image container
        self.get(self.page_url)
        container = find_element(self.browser, '#image-container')
        assert container is not None

        # please be sure to add items are added!
        cards = find_elements_all(container, '.v-card')
        assert len(cards) > 0

        # all images are linked to its detail page
        for card in cards:
            link = find_element(card, '.v-btn')
            assert check_url_pattern(link.get_attribute('href'), HistoryDetailPageTest.pattern)

    def test_user_want_more_images(self):
        # user click 'more' button to get more images

        # axios(or ajax) will bring more data without re-loading page

        # user find out that count of image increased

        pass


class HistoryDetailPageTest(PageLayoutTestMixin):
    """
    tests for /history/:id, user submitted image detail with specific information about it
    """
    @staticmethod
    def page_url(item=1):  # /history/:item
        return f'/history/{item}'

    pattern = re.compile(r'^/history/\d+$')

    def test_page_well_served(self):
        self.get(self.page_url())
        assert 'Take a Look' in self.browser.title

    def test_page_includes_descriptions(self):
        # history includes its id number

        # and prediction model and result, user submitted label

        # and visualized information for it

        pass


class ModelPageTest(PageLayoutTestMixin):
    """
    tests for /model, list of machine learning models supported by server will be shown
    """
    page_url = '/model'
    pattern = re.compile(r'^/model$')

    def test_page_well_served(self):
        self.get(self.page_url)
        assert 'Take a Look' in self.browser.title

    def test_user_browse_models(self):
        # user look around for available ML models

        # and is linked to its detail page

        pass


class ModelDetailPageTest(PageLayoutTestMixin):
    """
    tests for /model/:name, where detailed description of ML model provided
    it is likely to include some visualization components
    """
    @staticmethod
    def page_url(name='svm'):
        return f'/model/{name}'

    pattern = re.compile(r'^/model/\w+$')

    def test_page_well_served(self):
        self.get(self.page_url())
        assert 'Take a Look' in self.browser.title

    def test_page_include_spec_description(self):
        # model spec includes description about it

        # and metadata, like hyperparameter or sth for model

        # and visualized info

        pass


class PredictPageTest(PageLayoutTestMixin):
    """
    tests for /predict, where user uploads image for prediction
    """
    page_url = '/predict'
    pattern = re.compile(r'^/predict$')

    def test_user_request_for_prediction(self):
        # user select image file and model to use for test

        # user submit the request and wait for prediction done
        # and form will be blocked for 10 seconds

        # will receive url for result when the job is done

        pass

    def test_user_try_wrong_request(self):
        # user forgot to fill some data for request but try to send it

        # an error message will be shown and no request will be made

        pass
