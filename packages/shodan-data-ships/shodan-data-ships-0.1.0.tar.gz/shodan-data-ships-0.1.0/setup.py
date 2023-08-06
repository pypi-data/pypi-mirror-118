# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shodan_data_ships']

package_data = \
{'': ['*']}

install_requires = \
['httpx[http2,brotli]>=0.19.0,<0.20.0', 'pydantic>=1.8.2,<2.0.0']

setup_kwargs = {
    'name': 'shodan-data-ships',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
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
