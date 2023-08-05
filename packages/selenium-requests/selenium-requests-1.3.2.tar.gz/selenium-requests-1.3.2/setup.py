# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['seleniumrequests']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0',
 'selenium>=3.141.0,<4.0.0',
 'tldextract>=3.1.1,<4.0.0']

setup_kwargs = {
    'name': 'selenium-requests',
    'version': '1.3.2',
    'description': 'Extends Selenium WebDriver classes to include the request function from the Requests library, while doing all the needed cookie and request headers handling.',
    'long_description': None,
    'author': 'Chris Braun',
    'author_email': 'cryzed@googlemail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)
