""" /functional_test.py
    integration testing for overall system

    this mainly tests hypermedia behaviors for user (front-end)

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
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as Wait
from test_helper import (
    check_url_pattern,  # use compiled pattern in repeated tests
)


@pytest.fixture(scope='session')
def browser():
    browser = webdriver.Chrome(os.environ.get('SELENIUM_WEBDRIVER_CHROME', 'C:/Tools/chromedriver.exe'))
    browser.implicitly_wait(1)
    yield browser
    browser.quit()


@pytest.mark.functional
@pytest.mark.frontend
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
        footer = self.browser.find_element_by_id('footer')
        assert 'Take a Look' in footer.text

    def test_bottom_navbar_works_well(self):
        # user look layouts, especially our simple & fancy bottom bar
        self.get(self.page_url)
        navbar = self.browser.find_element_by_id('bottom-navbar')
        assert navbar

        # using 'navbar' instead of 'self.browser' to make sure that link is child of navbar
        for (selector, url_pattern) in [('navbar-link-home', IndexPageTest.pattern),
                                        ('navbar-link-model', ModelPageTest.pattern),
                                        ('navbar-link-predict', PredictPageTest.pattern)]:
            link = navbar.find_element_by_id(selector)
            assert check_url_pattern(link.get_attribute('href'), url_pattern)


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
        carousel = self.browser.find_element_by_id('recent-submits')
        assert carousel

        # carousel should include at least one image, even tough there's nothing in database
        items = carousel.find_elements_by_css_selector('.v-window-item')
        assert len(items) > 0, 'Carousel must contain at least one image'

    def test_simple_descriptions_of_models_provided(self):
        # finally user arrived at our models's preview
        # it is some kind of drawer component, or accordion, or something like that
        self.get(self.page_url)
        preview = self.browser.find_element_by_id('model-previews')
        assert preview

        # our selenium tester will test all models in the container
        # model should be shown at least one
        models = preview.find_elements_by_css_selector('.v-expansion-panel')
        assert len(models) > 0, 'No model preview provided'


class ModelPageTest(PageLayoutTestMixin):
    """
    tests for /model, user submitted image list page
    """
    page_url = '/model'
    pattern = re.compile(r'^/model$')

    def test_models_available(self):
        # models are gathered at model container
        container = self.browser.find_element_by_id('model-container')
        assert container

        # check is there any model in page
        models = container.find_elements_by_css_selector('.v-tab')
        assert len(models) > 0, 'No model provided; add it'

    def test_open_dialog_for_history_detail(self):
        # user get to history page to look around some kitty images, for time killing or whatever
        # and find the image container
        self.get(self.page_url)
        container = self.browser.find_element_by_id('image-container')
        assert container

        # when user clicks image, modal for this image will be popped up and will load data via AJAX
        # test all of it for fixture we provided
        cards = container.find_elements_by_css_selector('.v-card')[:5]
        assert len(cards) > 0, 'No history yet'

    def test_load_more_contents(self):
        self.get(self.page_url)
        container = self.browser.find_element_by_id('image-container')
        assert container

        # please be sure to add items are added!
        cards = container.find_elements_by_css_selector('.v-card')
        assert len(cards) > 0, 'No history in page; plz add it'

        # user find button 'more'
        btn = container.find_element_by_id('more-btn')
        assert btn is not None

        # and click it, then new cards will be present on window
        btn.click()
        old_card_count = len(cards)
        card_brought = Wait(container, 5).until(
            lambda c: len(c.find_elements_by_css_selector('.v-card')) - old_card_count,
            message='Could not detect any change in history catalog'
        )
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
        prediction_form = self.browser.find_element_by_id('prediction-form')
        assert prediction_form

        # select image
        upload_image = prediction_form.find_element_by_id('upload-image')
        assert upload_image
        upload_image.send_keys('C:/Users/dldbc/Downloads/sample_image.jpg')

        # and label for it
        label_of_item = prediction_form.find_element_by_id('select-label')
        assert label_of_item
        label_of_item.send_keys('Cat')

        # select model for prediction
        model_to_use = prediction_form.find_element_by_id('select-model')
        assert model_to_use
        model_to_use.send_keys('SVM')

        # user submit the request and wait for prediction done
        form_submit = Wait(prediction_form, 3).until(
            EC.element_to_be_clickable((By.ID, 'request-submit')),
            message='Submit button is not clickable'
        )
        assert form_submit
        form_submit.click()

        # user will receive url for result when the job is done
        result_sign = self.browser.find_element_by_id('result-sign')
        old_text = result_sign.text
        is_changed = Wait(result_sign, 10).until(
            lambda e: e.text != old_text,
            message='Status feedback not changing'
        )
        assert is_changed

    def test_user_try_wrong_request(self):
        # user forgot to fill some data for request but try to send it

        # an error message will be shown and no request will be made

        pass
