# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['py_sanic_samples',
 'py_sanic_samples.api',
 'py_sanic_samples.api.content',
 'py_sanic_samples.config']

package_data = \
{'': ['*']}

install_requires = \
['jupyterlab>=3.1.9,<4.0.0',
 'sanic-openapi>=21.6.1,<22.0.0',
 'sanic>=21.6.2,<22.0.0']

setup_kwargs = {
    'name': 'py-sanic-samples',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': '李国冬',
    'author_email': 'liguodongiot@163.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
