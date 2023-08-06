# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scrapinsta',
 'scrapinsta.domain',
 'scrapinsta.domain.entities',
 'scrapinsta.domain.providers',
 'scrapinsta.infra',
 'scrapinsta.infra.entities',
 'scrapinsta.infra.entities.tests',
 'scrapinsta.infra.providers',
 'scrapinsta.infra.providers.tests']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=3.4.8,<4.0.0',
 'selenium>=3.141.0,<4.0.0',
 'webdriver-manager>=3.4.2,<4.0.0']

setup_kwargs = {
    'name': 'scrapinsta',
    'version': '0.0.3b0',
    'description': 'A package to scraping data from Instagram',
    'long_description': None,
    'author': 'Matheus Kolln',
    'author_email': 'matheuzhenrik@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
