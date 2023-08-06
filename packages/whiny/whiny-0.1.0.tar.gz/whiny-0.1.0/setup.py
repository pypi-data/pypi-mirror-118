# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['whiny']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['whiny = whiny.__main__:Foo']}

setup_kwargs = {
    'name': 'whiny',
    'version': '0.1.0',
    'description': "Simple validation leveraging Python's descriptor protocol.",
    'long_description': '<div align="center">\n\n<h1>Whiny</h1>\n<strong>>> <i>Simple validation leveraging Python\'s descriptor protocol.</i> <<</strong>\n\n&nbsp;\n\n</div>\n\n![img](https://user-images.githubusercontent.com/30027932/122619075-6a87b700-d0b1-11eb-9d6b-355446910cc1.png)\n\n\n\n## Status\n\nUnder construction...\n\n<div align="center">\n<i> ✨ 🍰 ✨ </i>\n</div>\n',
    'author': 'rednafi',
    'author_email': 'redowan.nafi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rednafi/whiny',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
