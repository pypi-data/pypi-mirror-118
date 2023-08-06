# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['comic_html_view_generator']

package_data = \
{'': ['*'],
 'comic_html_view_generator': ['test_output_volume/simulated_comic_volume_001/issue001/*',
                               'test_output_volume/simulated_comic_volume_001/issue002/*']}

entry_points = \
{'console_scripts': ['comic_html_view_generator = '
                     'comic_html_view_generator.chvg:main']}

setup_kwargs = {
    'name': 'comic-html-view-generator',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'Leland Batey',
    'author_email': 'lelandbatey@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
