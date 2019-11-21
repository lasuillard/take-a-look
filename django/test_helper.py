""" /test_helper.py
    helper classes and functions for tests, mainly functional test with selenium webdriver
"""

import re
import pytest
from urllib.parse import urljoin, urlparse
from selenium.common.exceptions import NoSuchElementException


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


def check_url_pattern(url, pattern):
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


def find_element_by_css_selector(element, selector, default=None):
    try:
        target = element.find_element_by_css_selector(selector)
    except NoSuchElementException:
        return default
    else:
        return target


def find_elements_by_css_selector(element, selector, default=None):
    targets = element.find_elements_by_css_selector(selector)
    if len(targets) == 0:
        return default if default is not None else []

    return targets
