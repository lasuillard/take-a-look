""" /functional_test.py
    integration testing for overall system
"""
import pytest
from selenium import webdriver


@pytest.mark.django_db(transaction=True)
class IndexPageTest:
    server_url = 'http://localhost:80'

    @classmethod
    def setup_class(cls):
        cls.browser = webdriver.Chrome('C:/Tools/chromedriver.exe')
        cls.browser.implicitly_wait(5.0)

    @classmethod
    def teardown_class(cls):
        cls.browser.quit()

    def test_page_served_well(self):
        self.browser.get(f'{self.server_url}/')
        assert 'Tomcat' in self.browser.title
