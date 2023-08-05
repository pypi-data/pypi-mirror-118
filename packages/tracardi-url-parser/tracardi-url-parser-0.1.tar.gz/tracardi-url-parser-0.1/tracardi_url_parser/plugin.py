from tracardi_dot_notation.dot_accessor import DotAccessor
from tracardi_plugin_sdk.domain.register import Plugin, Spec, MetaData
from tracardi_plugin_sdk.action_runner import ActionRunner
from tracardi_plugin_sdk.domain.result import Result

import urllib
from urllib.parse import urlparse


class ParseURLParameters(ActionRunner):

    def __init__(self, **kwargs):
        if 'url' not in kwargs or kwargs['url'] is None:
            raise ValueError("Please define url location as dot notation path.")

        self.url = kwargs['url']

    async def run(self, void):
        if not isinstance(self.session.context, dict):
            raise KeyError("No session context defined.")

        dot = DotAccessor(self.profile, self.session, None, self.event, self.flow)
        page_url = dot[self.url]

        parsed = urlparse(page_url)
        params = urllib.parse.parse_qsl(parsed.query)

        result = {
            'url': page_url,
            'scheme': parsed.scheme,
            'hostname': parsed.hostname,
            'path': parsed.path,
            'query': parsed.query,
            'params': {k: v for k, v in params},
            'fragment': parsed.fragment
        }

        return Result(port="payload", value=result)


def register() -> Plugin:
    return Plugin(
        start=False,
        spec=Spec(
            module='tracardi_url_parser.plugin',
            className='ParseURLParameters',
            inputs=['void'],
            outputs=['payload'],
            init={
                'url': 'session@context.page.url'
            }
        ),
        metadata=MetaData(
            name='Parse URL',
            desc='Reads URL parameters form context, parses it and returns as dictionary.',
            type='flowNode',
            width=200,
            height=100,
            icon='json',
            group=["Operations"]
        )
    )
