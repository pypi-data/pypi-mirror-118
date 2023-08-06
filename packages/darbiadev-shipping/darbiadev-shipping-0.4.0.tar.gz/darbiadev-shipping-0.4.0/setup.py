# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['darbiadev_shipping']

package_data = \
{'': ['*']}

extras_require = \
{'docs': ['sphinx>=4.1.1,<5.0.0',
          'sphinxcontrib-napoleon>=0.7,<0.8',
          'sphinxcontrib-autoprogram>=0.1.7,<0.2.0',
          'sphinx-rtd-theme>=0.5.2,<0.6.0',
          'toml>=0.10.2,<0.11.0'],
 'fedex': ['darbiadev-fedex>=0.3.0,<0.4.0'],
 'tests': ['pytest>=6.2.4,<7.0.0', 'tox>=3.24.0,<4.0.0'],
 'ups': ['darbiadev-ups>=0.5.0,<0.6.0'],
 'usps': ['darbiadev-usps>=0.5.0,<0.6.0']}

setup_kwargs = {
    'name': 'darbiadev-shipping',
    'version': '0.4.0',
    'description': 'darbiadev-shipping',
    'long_description': "# darbiadev-shipping\n\nA package wrapping multiple shipping carrier API wrapping packages, providing a higher level multi carrier package.\n\nDocumentation is hosted [here](https://darbiadev.github.io/darbiadev-shipping/)\n\nExample usage:\n```python\nfrom darbiadev_shipping import ShippingServices\n\nclient = ShippingServices(\n    ups_auth={\n        'base_url': '',\n        'username': '',\n        'password': '',\n        'access_license_number': '',\n    },\n    fedex_auth={\n        'web_service_url': '',\n        'key': '',\n        'password': '',\n        'account_number': '',\n        'meter_number': '',\n    },\n    usps_auth={\n        'base_url': '',\n        'user_id': '',\n        'password': '',\n    }\n)\n\nprint(client.track('1Z5338FF0107231059'))\n```\n",
    'author': 'Bradley Reynolds',
    'author_email': 'bradley.reynolds@darbia.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/darbiadev/darbiadev-shipping',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
