# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['_spock', 'spock']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=6.2.4,<7.0.0']

entry_points = \
{'pytest11': ['spock = _spock.plugin']}

setup_kwargs = {
    'name': 'pyspock',
    'version': '0.2.0',
    'description': 'Python implementation for spock framework',
    'long_description': '# spock\n\n<div align="center">\n  <a href="https://github.com/zen-xu/spock/actions">\n    <img src="https://github.com/zen-xu/spock/actions/workflows/main.yaml/badge.svg" alt="CI"/>\n  </a>\n  <a href="https://codecov.io/gh/zen-xu/spock">\n    <img src="https://codecov.io/gh/zen-xu/spock/branch/main/graph/badge.svg?token=WPG2V9w16r"/>\n  </a>\n  <a href="https://pypi.org/project/pyspock">\n    <img alt="PyPI" src="https://img.shields.io/pypi/v/pyspock">\n  </a>\n  <img src="https://img.shields.io/pypi/pyversions/pyspock">\n  <a href="https://github.com/zen-xu/spock/blob/main/LICENSE">\n    <img src="https://img.shields.io/badge/MIT%202.0-blue.svg" alt="License">\n  </a>\n</div>\n<div align="center">\n  <a href="https://results.pre-commit.ci/latest/github/zen-xu/spock/main">\n    <img src="https://results.pre-commit.ci/badge/github/zen-xu/spock/main.svg">\n  </a>\n  <a href="https://github.com/psf/black">\n    <img src="https://img.shields.io/badge/code%20style-black-000000.svg">\n  </a>\n  <a href="https://deepsource.io/gh/zen-xu/spock/?ref=repository-badge}" target="_blank">\n    <img alt="DeepSource" title="DeepSource" src="https://deepsource.io/gh/zen-xu/spock.svg/?label=active+issues&show_trend=true&token=mgZ7FgiJDAxSt9Ilav9vLFEo"/>\n  </a>\n</div>\n',
    'author': 'ZhengYu, Xu',
    'author_email': 'zen-xu@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
