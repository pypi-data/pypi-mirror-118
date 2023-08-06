# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['newscatcherapi']

package_data = \
{'': ['*']}

install_requires = \
['pendulum>=1.4,<2.0']

setup_kwargs = {
    'name': 'newscatcherapi',
    'version': '0.2.2',
    'description': 'NewsCatcher News API V2 SDK for Python',
    'long_description': "# NewsCatcher News API V2 SDK for Python\n\nThe official Python client library to manipulate NewsCatcher News API V2 from your Python application.\n\nDocumentation is identical with the API documentation. The same parameters and filters are available. \nAnd the same response structure. You can have a look at [docs.newscatcherapi.com](https://docs.newscatcherapi.com/).\n\n## Authentication\n\nThe Authentication is done via the `x_api_key` variable.\n\nReceive your API key by registering at [app.newscatcherapi.com](https://app.newscatcherapi.com/).\n\n## Installation\n```pip install newscatcherapi```\n\n## Quick Start\nImport installed package.\n\n`````from newscatcherapi import NewsCatcherApiClient`````\n\nInit the instance with an API key given after registration.\n\n````newscatcherapi = NewsCatcherApiClient(x_api_key='YOUR_API_KEY') ````\n\n## Endpoints\nAn instance of `NewsCatcherApiClient` has three main methods that correspond to three endpoints available for NewsCatcher News API.\n\n### Get News (/v2/search)\nMain method that allows you to find news article by keyword, date, language, country, etc.\n\n```\nall_articles = newscatcherapi.get_search(q='Elon Musk',\n                                         lang='en',\n                                         country='CA',\n                                         page_size=100)\n```\n\n### Get Latest Headlines (/v2/latest_headlines)\nGet the latest headlines given any topic, country, sources, or language.\n\n```\ntop_headlines = newscatcherapi.get_latest_headlines(lang='en',\n                                                    countries='us',\n                                                    topic='business')\n ```\n\n### Get Sources (/v2/sources)\nReturns a list of the top 100 supported news websites. Overall, we support over 60,000 websites. Using this method, you may find the top 100 for your specific language, country, topic combination.\n\n```\nsources = newscatcherapi.get_sources(topic='business',\n                                     lang='en',\n                                     countries='US')\n ```\n\n\n### Use *from_* and *to_* instead of *from* and *to* like in NewsCatcher News API\nIn Python, we are not allowed to reserve variable names *from* and *to*. If you try to use them, you will get a syntax error:\n\n```SyntaxError: invalid syntax``` \n\nSo, here is an example on how to use time variables *from_* and *to_* in *get_search* method.\n\n```\nall_articles = newscatcherapi.get_search(q='Elon Musk',\n                                         lang='en',\n                                         countries='CA,US',\n                                         from_='2021/08/20',\n                                         to_='2021/08/31')\n```\n\n## Feedback\n\nFeel free to contact us if you have spot a bug or have any suggestion at maksym`[at]`newscatcherapi.com",
    'author': 'Maksym Sugonyaka',
    'author_email': 'maksym@newscatcherapi.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://newscatcherapi.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
