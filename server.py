"""
Main server file
"""

import re
import urllib.parse as url_parsers

import aiohttp
from aiohttp import web

import tools
import configs

from bs4 import BeautifulSoup

HOST = configs.HOST


def middleware(actions: list):
    """ Middleware decorator """

    def wrap(func):
        async def wrapped(request):
            response = await func(request)
            for action in actions:
                action(response)

            return response
        return wrapped
    return wrap


def process_response(response: aiohttp.web.Response) -> web.Response:
    """ Special preprocessor for processing response text and links """

    if 'text/html' in response.content_type:
        soup = tools.url_replacer(BeautifulSoup(response.body, "html.parser"))

        targets = list(
            filter(
                lambda x: all(map(lambda y: y not in configs.SYSTEM_CHARACTERS, x)),
                soup.find_all(text=re.compile(configs.REGEX_PATTERN))
            )
        )
        tools.article_text_modifier(targets)
        response.body = str(soup).encode()

    return response


async def fetch(session: aiohttp.client.ClientSession, url: str) -> tuple:
    """ Middleware for articles """
    async def subfetch(url, subdomain_url):
        parsed = url_parsers.urlparse(url)
        replaced = parsed._replace(netloc=subdomain_url)
        url = replaced.geturl()
        # get acknowledged if server has required url
        res = await session.head(url)
        return res, url

    async with session.get(url) as response:
        if response.status != 200:
            for subdomain in configs.SUBDOMAINS:
                res, new_url = await subfetch(url, subdomain)
                if res.status != 404:
                    return await fetch(session, new_url)
                else:
                    continue

        content_type = response.content_type
        body = await response.read()
        return body, content_type


@middleware(actions=[process_response])
async def handle(request: web.Request) -> web.Response:
    """ Middleware for articles handling"""

    route = request.url.path
    async with aiohttp.ClientSession() as session:
        html, content_type = await fetch(session, f'{HOST}{route}')
    return web.Response(body=html, content_type=content_type)


app = web.Application()
app.router.add_route('*', '/{tail:.*}', handle)


if __name__ == "__main__":
    assert type(configs.REPLACE_URLS) == list
    assert len(configs.SYMBOL_TO_APPEND) == 1
    assert configs.REGEX_PATTERN

    web.run_app(app)
