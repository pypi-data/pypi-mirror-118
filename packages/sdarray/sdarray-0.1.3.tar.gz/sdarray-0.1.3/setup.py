# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sdarray']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sdarray',
    'version': '0.1.3',
    'description': 'Common single-dish data structure for radio astronomy',
    'long_description': '# sdarray\n\n[![PyPI](https://img.shields.io/pypi/v/sdarray.svg?label=PyPI&style=flat-square)](https://pypi.org/pypi/sdarray/)\n[![Python](https://img.shields.io/pypi/pyversions/sdarray.svg?label=Python&color=yellow&style=flat-square)](https://pypi.org/pypi/sdarray/)\n[![Tests](https://img.shields.io/github/workflow/status/sdarray/sdarray/Tests?logo=github&label=Tests&style=flat-square)](https://github.com/sdarray/sdarray/actions)\n[![License](https://img.shields.io/badge/license-MIT-blue.svg?label=License&style=flat-square)](LICENSE)\n\nCommon single-dish data structure for radio astronomy\n',
    'author': 'Akio Taniguchi',
    'author_email': 'taniguchi@a.phys.nagoya-u.ac.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sdarray/sdarray',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
