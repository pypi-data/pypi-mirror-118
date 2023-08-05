# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['npspy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'npspy',
    'version': '0.1.0',
    'description': '',
    'long_description': '# npspy\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nnpspy is a simple package to calculate [NPS](https://en.wikipedia.org/wiki/Net_promoter_score) (Net Promoter Score).\n\n\n## Install\n```\npip install npspy\n```\n\n## Example\n\n```python\nimport npspy\n\nnpspy.categorize(0)  # "detractor"\nnpspy.categorize(7)  # "passive"\nnpspy.categorize(9)  # "promoter"\n\nnpspy.calculate([0, 7, 9])  # 0\nnpspy.calculate([7, 9])  # 50\nnpspy.calculate([0, 7])  # -50\n```\n',
    'author': 'dr666m1',
    'author_email': 'skndr666m1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
