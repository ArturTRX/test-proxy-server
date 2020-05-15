"""
Main server file
"""

import re

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
        system_characters = ['<', '>', '|', '/', '"']
        soup = tools.url_replacer(BeautifulSoup(response.body, "html.parser"))

        targets = list(
            filter(
                lambda x: any(map(lambda y: y not in system_characters, x)),
                soup.find_all(text=re.compile(configs.REGEX_PATTERN))
            )
        )
        tools.article_text_modifier(targets)
        response.body = str(soup).encode()

    return response


async def fetch(session: aiohttp.client.ClientSession, url: str) -> tuple:
    """ Middleware for articles """

    async with session.get(url) as response:
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


async def ajax_mock(request: web.Request) -> web.Response:  # pylint: disable=unused-argument
    """ Handler for mocking ajax response """

    return web.Response()

app = web.Application()
app.router.add_route('*', '/forums/topic/{name}', handle)

app.router.add_route('*', '/ajax-impressions-track/', ajax_mock)

if __name__ == "__main__":
    web.run_app(app)
