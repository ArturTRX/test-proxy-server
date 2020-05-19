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
    tags_with_attributes = [
        ('a', 'href'),
        ('a', 'style'),
        ('img', 'src'),
        ('img', 'srcset'),

        ('meta', 'content'),
        ('link', 'href'),
        ('script', 'src'),
        ('span', 'style'),
        ('form', 'action'),
        ('option', 'value')
    ]

    for tag, attr in tags_with_attributes:
        for matched_tag in soup.findAll(tag):
            if matched_tag.get(attr):
                for url in configs.REPLACE_URLS:
                    matched_tag[attr] = matched_tag[attr].replace(url, "")
                matched_tag['target'] = None
    return soup
