"""
Tests for text modifiers
"""

import unittest
import bs4
import regex

import tools
import configs


class TestTextModifiers(unittest.TestCase):
    """ Test class for text modifier """

    def setUp(self) -> None:
        html = \
            '<head> ' \
            '<meta content="Всем ...привет((. Случилась очень неприятная ситуация, и ><<<данной< темой хотел ' \
            'предупредить остальных об очередных !новыых! идеяхх! этого оператора о том как ]___]]_)нагрет().' \
            '</head>'
        self.soup = bs4.BeautifulSoup(html, "html.parser")
        self.targets = list(
            filter(
                lambda x: any(map(lambda y: y not in configs.SYSTEM_CHARACTERS, x)),
                self.soup.find_all(text=regex.compile(configs.REGEX_PATTERN))
            )
        )

    def test_1_article_text_modifier(self):
        """ Valid test cases for article """
        tools.article_text_modifier(self.targets)

        self.assertEqual(len(self.soup.text), 198)
        self.assertEqual(
            self.soup.text,
            ' <meta content="Всем ...привет™((. Случилась очень неприятная ситуация, и ><<<данной™< темой хотел '
            'предупредить остальных об очередных !новыых™! идеяхх™! этого оператора о том как ]___]]_)нагрет™().'
        )

    def test_2_element_modifier(self):
        """ Valid test cases for element """
        self.assertEqual(tools.element_modifier('привет'), 'привет™')
        self.assertEqual(tools.element_modifier('..привет..'), '..привет™..')
        self.assertEqual(tools.element_modifier('_.!привет).'), '_.!привет™).')

        self.assertEqual(tools.element_modifier('Приветик'), 'Приветик')  # more than 6 symbols
        self.assertEqual(tools.element_modifier('Доров'), 'Доров')  # less than 6 symbols


if __name__ == '__main__':
    unittest.main()
