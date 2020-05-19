"""
Tests for html modifiers
"""

import unittest
import bs4
import tools
import configs


class TestHTMLModifiers(unittest.TestCase):
    """ Test class for html modifier """

    def setUp(self) -> None:
        """
        Setting up values for tests
        """

        configs.REPLACE_URLS = ["https://dou.ua", "https://jobs.dou.ua"]

    def test_1_valid_replace_case(self):
        """ Valid case """

        html = '<a href="https://dou.ua/"></a>'
        soup = bs4.BeautifulSoup(html, "html.parser")
        tools.url_replacer(soup)
        self.assertEqual(soup.findAll('a')[0]['href'], '/')

    def test_2_valid_replace_case(self):
        """ Valid case """

        html = '<a href="https://jobs.dou.ua/12344"></a>'
        soup = bs4.BeautifulSoup(html, "html.parser")
        tools.url_replacer(soup)
        self.assertEqual(soup.findAll('a')[0]['href'], '/12344')

    def test_3_invalid_replace_case(self):
        """ Invalid case """

        html = '<a href="https://google.com/12344"></a>'  # google not in configs.REPLACE_URLS
        soup = bs4.BeautifulSoup(html, "html.parser")
        tools.url_replacer(soup)
        self.assertNotEqual(soup.findAll('a')[0]['href'], '/12344')
        self.assertEqual(soup.findAll('a')[0]['href'], 'https://google.com/12344')


if __name__ == '__main__':
    unittest.main()
