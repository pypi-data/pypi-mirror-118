# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['flask_aserto']

package_data = \
{'': ['*']}

install_requires = \
['aserto>=0.1.1,<0.2.0', 'typing-extensions>=3.10.0,<4.0.0']

setup_kwargs = {
    'name': 'flask-aserto',
    'version': '0.1.0',
    'description': 'Aserto integration for Flask',
    'long_description': None,
    'author': 'Aserto, Inc.',
    'author_email': 'pypi@aserto.com',
    'maintainer': 'authereal',
    'maintainer_email': 'authereal@aserto.com',
    'url': 'https://github.com/aserto-dev/aserto-python/tree/HEAD/packages/flask-aserto',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
