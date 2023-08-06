# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['video_to_slides']

package_data = \
{'': ['*']}

install_requires = \
['PyMuPDF>=1.18.17,<2.0.0',
 'opencv-python>=4.5.3,<5.0.0',
 'pytesseract>=0.3.8,<0.4.0',
 'rapidfuzz>=1.5.0,<2.0.0',
 'tesseract>=0.1.3,<0.2.0']

entry_points = \
{'console_scripts': ['video-to-slides = video_to_slides:cli']}

setup_kwargs = {
    'name': 'video-to-slides',
    'version': '0.1.0',
    'description': 'Convert video to pdf slides.',
    'long_description': None,
    'author': '0scarB',
    'author_email': 'oscarb@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/0scarB/video-to-slides',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
