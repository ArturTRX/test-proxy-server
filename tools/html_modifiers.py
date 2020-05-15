"""
Module of tools, that modify html
"""

import bs4
import configs

__all__ = \
    [
        'url_replacer'
    ]


def url_replacer(soup: bs4.BeautifulSoup) -> bs4.BeautifulSoup:
    """ Function for replacing urls at page """

    for a_tag in soup.findAll('a'):
        if a_tag.get('href'):
            for url in configs.REPLACE_URLS:
                a_tag['href'].replace(url, "")
            a_tag['target'] = None
    return soup
