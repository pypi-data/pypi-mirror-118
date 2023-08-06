# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['requests_ratelimiter']

package_data = \
{'': ['*']}

install_requires = \
['pyrate-limiter>=2.3,<3.0', 'requests>=2.20,<3.0']

extras_require = \
{'docs': ['furo==2021.8.17b43',
          'myst-parser>=0.15.1,<0.16.0',
          'sphinx>=4.0.2,<5.0.0',
          'sphinx-autodoc-typehints>=1.11,<2.0',
          'sphinx-copybutton>=0.3,<0.5']}

setup_kwargs = {
    'name': 'requests-ratelimiter',
    'version': '0.2.1',
    'description': 'Rate-limiting for the requests library',
    'long_description': '# Requests-Ratelimiter\n[![Build\nstatus](https://github.com/JWCook/requests-ratelimiter/workflows/Build/badge.svg)](https://github.com/JWCook/requests-ratelimiter/actions)\n[![Documentation Status](https://img.shields.io/readthedocs/requests-ratelimiter/stable?label=docs)](https://requests-ratelimiter.readthedocs.io)\n[![PyPI](https://img.shields.io/pypi/v/requests-ratelimiter?color=blue)](https://pypi.org/project/requests-ratelimiter)\n[![PyPI - Python Versions](https://img.shields.io/pypi/pyversions/requests-ratelimiter)](https://pypi.org/project/requests-ratelimiter)\n[![PyPI - Format](https://img.shields.io/pypi/format/requests-ratelimiter?color=blue)](https://pypi.org/project/requests-ratelimiter)\n\nThis package is a thin wrapper around [pyrate-limiter](https://github.com/vutran1710/PyrateLimiter)\nthat adds convenient integration with the [requests](https://github.com/psf/requests) library.\n\nProject documentation can be found at [requests-ratelimiter.readthedocs.io](https://requests-ratelimiter.readthedocs.io).\n\n\n## Features\n* `pyrate-limiter` implements the leaky bucket algorithm, supports multiple rate limits, and an\n  optional Redis backend\n* `requests-ratelimiter` can be used as a\n  [transport adapter](https://docs.python-requests.org/en/master/user/advanced/#transport-adapters),\n  [session](https://docs.python-requests.org/en/master/user/advanced/#session-objects),\n  or session mixin for compatibility with other `requests`-based libraries.\n* Rate limits can be automatically tracked separately per host, and different rate limits can be\n  manually applied to different hosts\n\n## Installation\n```\npip install requests-ratelimiter\n```\n\n## Usage\n\n### Sessions\nExample with `LimiterSession`:\n\n```python\nfrom requests import Session\nfrom requests_ratelimiter import LimiterSession\n\n# Apply a rate-limit (5 requests per second) to all requests\nsession = LimiterSession(per_second=5)\n\n# Make rate-limited requests that stay within 5 requests per second\nfor _ in range(10):\n    response = session.get(\'https://httpbin.org/get\')\n    print(response.json())\n```\n\n### Adapters\nExample with `LimiterAdapter`:\n\n```python\nfrom requests import Session\nfrom requests_ratelimiter import LimiterAdapter\n\nsession = Session()\n\n# Apply a rate-limit (5 requests per second) to all requests\nadapter = LimiterAdapter(per_second=5)\nsession.mount(\'http://\', adapter)\nsession.mount(\'https://\', adapter)\n\n# Make rate-limited requests\nfor user_id in range(100):\n    response = session.get(f\'https://api.some_site.com/v1/users/{user_id}\')\n    print(response.json())\n```\n\n### Per-Host Rate Limits\nWith `LimiterAdapter`, you can apply different rate limits to different hosts or URLs:\n```python\n# Apply different rate limits (2/second and 100/minute) to a specific host\nadapter_2 = LimiterAdapter(per_second=2, per_minute=100)\nsession.mount(\'https://api.some_site.com\', adapter_2)\n```\n\nBehavior for matching requests is the same as other transport adapters: `requests` will use the\nadapter with the most specific (i.e., longest) URL prefix for a given request. For example:\n```python\nsession.mount(\'https://api.some_site.com/v1\', adapter_3)\nsession.mount(\'https://api.some_site.com/v1/users\', adapter_4)\n\n# This request will use adapter_3\nsession.get(\'https://api.some_site.com/v1/\')\n\n# This request will use adapter_4\nsession.get(\'https://api.some_site.com/v1/users/1234\')\n```\n\n### Per-Host Rate Limit Tracking\nWith either `LimiterSession` or `LimiterAdapter`, you can automatically track rate limits separately\nfor each host; in other words, requests sent to one host will not count against the rate limit for\nany other hosts. This can be enabled with the `per_host` option:\n\n```python\nsession = LimiterSession(per_second=5, per_host=True)\n\n# Make requests for two different hosts\nfor _ in range(10):\n    response = session.get(f\'https://httpbin.org/get\')\n    print(response.json())\n    session.get(f\'https://httpbingo.org/get\')\n    print(response.json())\n```\n\n## Compatibility\nThere are many other useful libraries out there that add features to `requests`, most commonly by\nextending or modifying\n[requests.Session](https://docs.python-requests.org/en/master/api/#requests.Session).\n\nTo use `requests-ratelimiter` with one of these libraries, you have at least two options:\n1. Mount a `LimiterAdapter` on an instance of the library\'s `Session` class\n2. Use `LimiterMixin` to create a custom `Session` class with features from both libraries\n\n### Requests-Cache\nFor example, to combine with [requests-cache](https://github.com/reclosedev/requests-cache), which\nalso includes a separate mixin class:\n```python\nfrom pyrate_limiter import RedisBucket\nfrom requests import Session\nfrom requests_cache import CacheMixin, RedisCache\nfrom requests_ratelimiter import LimiterMixin\n\n\nclass CachedLimiterSession(CacheMixin, LimiterMixin, Session):\n    """Session class with caching and rate-limiting behavior. Accepts arguments for both\n    LimiterSession and CachedSession.\n    """\n\n\n# Optionally use Redis as both the bucket backend and the cache backend\nsession = CachedLimiterSession(\n    per_second=5,\n    bucket_class=RedisBucket,\n    backend=RedisCache(),\n)\n```\n\nThis example has an extra benefit: cache hits won\'t count against your rate limit!\n',
    'author': 'Jordan Cook',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/JWCook/requests-ratelimiter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
