# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['netbox_dns',
 'netbox_dns.api',
 'netbox_dns.core',
 'netbox_dns.migrations',
 'netbox_dns.templatetags',
 'netbox_dns.tests']

package_data = \
{'': ['*'], 'netbox_dns': ['templates/netbox_dns/*']}

setup_kwargs = {
    'name': 'netbox-dns',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Aurora Research Lab',
    'author_email': 'info@aurorabilisim.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
