# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['requests_ratelimiter']

package_data = \
{'': ['*']}

install_requires = \
['pyrate-limiter>=2.3,<3.0', 'requests>=2.20,<3.0']

setup_kwargs = {
    'name': 'requests-ratelimiter',
    'version': '0.1.0',
    'description': 'Rate-limiting for the requests library',
    'long_description': 'None',
    'author': 'Jordan Cook',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
