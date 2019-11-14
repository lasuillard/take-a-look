""" /functional_test.py
    integration testing for overall system

    this mainly tests hypermedia behaviors for user (front-end)
"""
import pytest
import urllib.parse
from selenium import webdriver


@pytest.fixture(scope='module')
def browser():
    browser = webdriver.Chrome('C:/Tools/chromedriver.exe')
    yield browser
    browser.quit()


class WebBrowser:
    """
    helper class for functional tests with selenium webdriver
    """
    server_url = 'http://localhost:80'

    def get(self, browser, url):
        return browser.get(urllib.parse.urljoin(self.server_url, url))


class IndexPageTest(WebBrowser):
    """
    tests for /
    """
    def test_page_served_well(self, browser):
        self.get(browser, '/')
        assert 'Take a Look' in browser.title


class HistoryPageTest(WebBrowser):
    """

    """
    def test_page_served_well(self, browser):
        self.get(browser, '/history')
        assert 'Take a Look' in browser.title
