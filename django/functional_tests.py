""" /functional_test.py
    integration testing for overall system

    this mainly tests hypermedia behaviors for user (front-end)

    TODO:
    - url mapping for tomcat jsp files, {model/history}-detail


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

    def test_page_well_served(self):
        # user visit main page and find 'Take a Look' in title
        self.get(self.page_url)
        assert 'Take a Look' in self.browser.title

    def test_page_has_common_footer(self):
        # page has footer
        self.get(self.page_url)
        footer = find_element(self.browser, '#footer')
        assert footer is not None

    def test_bottom_navbar_works_well(self):
        # user look layouts, especially our simple & fancy bottom bar
        self.get(self.page_url)
        navbar = find_element(self.browser, '#bottom-navbar')
        assert navbar is not None

        # using 'navbar' instead of 'self.browser' to make sure that link is child of navbar
        for (selector, url_pattern) in [('#navbar-link-home', IndexPageTest.pattern),
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

    def test_page_has_carousel_linked_to_history(self):
        # user find image carousel
        self.get(self.page_url)
        carousel = find_element(self.browser, '#recent-submits')
        assert carousel is not None

    def test_simple_descriptions_of_models_provided(self):
        # finally user arrived at our models's preview
        # it is some kind of drawer component, or accordion, or something like that
        self.get(self.page_url)
        preview = find_element(self.browser, '#model-previews')
        assert preview is not None

        # our selenium tester will test all models in the container
        # model should be shown at least one
        models = find_elements_all(preview, '.v-expansion-panel')
        assert len(models) > 0


class ModelPageTest(PageLayoutTestMixin):
    """
    tests for /history, user submitted image list page
    """
    page_url = '/model'
    pattern = re.compile(r'^/model$')

    def test_models_available(self):
        # models are gathered at model container
        container = find_element(self.browser, '#model-container')
        assert container is not None

        # check is there any model in page
        models = find_elements_all(container, '.v-')
        assert len(models) > 0, 'No model provided; add it'

        # user check model by its modal window
        assert False, 'Test is not done'

    def test_open_dialog_for_history_detail(self):
        # user get to history page to look around some kitty images, for time killing or whatever
        # and find the image container
        self.get(self.page_url)
        container = find_element(self.browser, '#image-container')
        assert container is not None

        # when user clicks image, modal for this image will be popped up and will load data via AJAX
        # test all of it for fixture we provided
        cards = find_elements_all(container, '.v-card')
        for card in cards:
            btn_detail = find_element(card, '.v-btn')
            assert btn_detail is not None

        # how to test modal?
        pass

    def test_load_more_contents(self):
        self.get(self.page_url)
        container = find_element(self.browser, '#image-container')
        assert container is not None

        # please be sure to add items are added!
        cards = find_elements_all(container, '.v-card')
        assert len(cards) > 0, 'No history in page; plz add it'

        # user find button 'more'
        btn = find_element(container, '#more-btn')
        assert btn is not None

        # and click it, then new cards will be present on window
        btn.click()
        old_card_count = len(cards)
        card_brought = Wait(container, 5).until(lambda c: len(find_elements_all(c, '.v-card')) - old_card_count)
        assert card_brought > 0, 'Elements expected to increase; what have you done?'


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
