""" /test_helper.py
    helper classes and functions for tests, mainly functional test with selenium webdriver
"""

import re
from urllib.parse import urlparse
from selenium.common.exceptions import NoSuchElementException


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


def find_element(element, selector, move=True, default=None):
    """
    Find and return element found, and move to element if necessary
    """
    try:
        target = element.find_element_by_css_selector(selector)
    except NoSuchElementException:
        return default
    else:
        if move:
            _ = target.location_once_scrolled_into_view
        return target


def find_elements_all(element, selector, default=None):
    """
    Find elements all, returns empty string if found none
    """
    targets = element.find_elements_by_css_selector(selector)
    if len(targets) == 0:
        return default if default is not None else []

    return targets
