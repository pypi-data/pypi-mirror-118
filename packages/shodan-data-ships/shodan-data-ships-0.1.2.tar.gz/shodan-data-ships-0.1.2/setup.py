# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shodan_data_ships']

package_data = \
{'': ['*']}

install_requires = \
['httpx[brotli,http2]>=0.19.0,<0.20.0', 'pydantic>=1.8.2,<2.0.0']

setup_kwargs = {
    'name': 'shodan-data-ships',
    'version': '0.1.2',
    'description': 'Library for consuming data from the Open Ships data feed from Shodan',
    'long_description': '# Shodan Data: Ships\n\nA data feed of NMEA messages from open, public ship receivers on the Internet.\n\nOpenAPI Specification: https://ships.data.shodan.io/openapi.json\n\n## Installation\n\n```shell\npip install shodan-data-ships\n```\n\n## Quickstart\n\nThe library provides both synchronous and asynchronous clients to the Ships datafeed. The easiest way to get started is using the synchronous interface:\n\n```python\nfrom shodan_data_ships.client import Client\n\n\nclient = Client("YOUR SHODAN API KEY")\nfor msg in client.messages():\n    print(msg)\n```\n\n## Data Schema\n\nFor the latest list of properties that are available please refer to the OpenAPI documentation at:\n\nhttps://ships.data.shodan.io/docs\n\nData models are generated from the above JSON schema and are available in the respective ``shodan_data_ships.model.NMEAMessage`` and ``shodan_data_ships.model.Receiver`` classes.\n\n## Asynchronous Client\n\nThe library also lets you subscribe to data using ``asyncio``. Simply use the ``shodan_data_ships.client.AsyncClient`` class:\n\n```python\nfrom shodan_data_ships.client import AsyncClient\n\n\nasync def main():\n    client = AsyncClient("YOUR SHODAN API KEY")\n\n    async for msg in client.messages():\n        print(msg)\n\n\nif __name__ == \'__main__\':\n    import asyncio\n    asyncio.run(main())\n```\n',
    'author': 'John Matherly',
    'author_email': 'jmath@shodan.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
