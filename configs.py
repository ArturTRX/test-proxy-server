"""
Main configs file
"""

HOST = 'https://dou.ua'

REPLACE_URLS = [
    "https://dou.ua", "https://jobs.dou.ua", "http://jobs.dou.ua", "https://s.dou.ua", "//s.dou.ua", "//dou.ua"
]

REGEX_PATTERN = r'\b\w{6}\b'

SYMBOL_TO_APPEND = '™'

SYSTEM_CHARACTERS = ['<', '>', '|', '/']

SUBDOMAINS = [
    's.dou.ua',
    'jobs.dou.ua'
]
