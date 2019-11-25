""" /functional_test.py
    integration testing for overall system

    this mainly tests hypermedia behaviors for user (front-end)

    TODO:
    - replace all find_element and find_elements_all with selenium default for consistency and readability
    - filtering supports on history


    testing strategies:
    - locate
        step 1. wide search: find elements by html id attribute
        step 2. narrow down: find vuetify components via html class, like: .v-expansion-panel-header
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
import random
from urllib.parse import urljoin
import pytest
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains as Action
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as Wait, Select
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
        assert footer

    def test_bottom_navbar_works_well(self):
        # user look layouts, especially our simple & fancy bottom bar
        self.get(self.page_url)
        navbar = find_element(self.browser, '#bottom-navbar')
        assert navbar

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
        assert carousel

    def test_simple_descriptions_of_models_provided(self):
        # finally user arrived at our models's preview
        # it is some kind of drawer component, or accordion, or something like that
        self.get(self.page_url)
        preview = find_element(self.browser, '#model-previews')
        assert preview

        # our selenium tester will test all models in the container
        # model should be shown at least one
        models = find_elements_all(preview, '.v-expansion-panel')
        assert len(models) > 0


class ModelPageTest(PageLayoutTestMixin):
    """
    tests for /model, user submitted image list page
    """
    page_url = '/model'
    pattern = re.compile(r'^/model$')

    def test_models_available(self):
        # models are gathered at model container
        container = find_element(self.browser, '#model-container')
        assert container

        # check is there any model in page
        models = find_elements_all(container, '.v-tab')
        assert len(models) > 0, 'No model provided; add it'

    def test_open_dialog_for_history_detail(self):
        # user get to history page to look around some kitty images, for time killing or whatever
        # and find the image container
        self.get(self.page_url)
        container = find_element(self.browser, '#image-container')
        assert container

        # when user clicks image, modal for this image will be popped up and will load data via AJAX
        # test all of it for fixture we provided
        cards = find_elements_all(container, '.v-card')
        for card in cards:
            # look for button to open dialog
            btn_detail = find_element(card, '.v-btn')
            assert btn_detail

            # click the button and check contents
            btn_detail.click()
            dialog = Wait(self.browser, 3).until(
                EC.visibility_of_element_located((By.ID, 'history-dialog')),
            )
            assert dialog

            # click close button and check dialog closed
            btn_close = Wait(self.browser, 3).until(EC.visibility_of_element_located((By.ID, 'close-dialog')))
            btn_close.click()
            is_closed = Wait(self.browser, 3).until(EC.invisibility_of_element(dialog))
            assert is_closed

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
        # find form first
        self.get(self.page_url)
        prediction_form = find_element(self.browser, '#prediction-form')
        assert prediction_form

        # select image
        upload_image = find_element(prediction_form, '#upload-image')
        assert upload_image
        upload_image.send_keys('C:/Users/dldbc/Downloads/sample_image.jpg')

        # and label for it
        label_of_item = find_element(prediction_form, '#select-label')
        assert label_of_item
        label_of_item.send_keys('Cat')

        # select model for prediction
        model_to_use = find_element(prediction_form, '#select-model')
        assert model_to_use
        model_to_use.send_keys('SVM')

        # user submit the request and wait for prediction done
        form_submit = Wait(prediction_form, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#request-submit')))
        assert form_submit
        form_submit.click()

        # user will receive url for result when the job is done
        result_sign = find_element(self.browser, '#result-sign')
        old_text = result_sign.text
        is_changed = Wait(result_sign, 10).until(lambda e: e.text != old_text)
        assert is_changed

    def test_user_try_wrong_request(self):
        # user forgot to fill some data for request but try to send it

        # an error message will be shown and no request will be made

        pass
