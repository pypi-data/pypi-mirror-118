# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['blinkcheck']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2,<3']

entry_points = \
{'console_scripts': ['blinkcheck = blinkcheck.console:main']}

setup_kwargs = {
    'name': 'blinkcheck',
    'version': '0.1.0',
    'description': 'Basic link checker',
    'long_description': '# 🌎 `blinkcheck` - a basic link checker\n\n[![Latest Release](https://img.shields.io/github/release/blu3r4y/blinkcheck.svg?style=popout-square)](https://github.com/blu3r4y/blinkcheck/releases/latest)\n[![PyPI Version](https://img.shields.io/pypi/v/blinkcheck?style=popout-square)](https://pypi.org/project/blinkcheck/)\n[![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg?style=popout-square)](LICENSE.txt)\n\nCheck for dead links in all files, with support for regex URL extraction and glob file patterns.\n\n## Installation\n\n    pip install blinkcheck\n\n## Usage Examples\n\nCheck for dead links in all files, starting in the current directory.\n\n    blinkcheck\n\nCheck for dead links in all Markdown `*.md` files of a specific `./docs` folder.\n\n    blinkcheck --root ./docs -i *.md\n\nCheck for dead links in LaTeX `*.tex` files in the current directory with regex `\\\\url{(.*?)}`.  \nIf a regex contains one group constructs, the group is used as the link.\n\n    blinkcheck -i *.tex -r "\\\\url{(.*?)}"\n\nOnly list failed links and do not verify SSL certificates.\n\n    blinkcheck --skip-ssl --only-fails\n\n## Available Arguments\n\n| Argument       | Default Value                                        | Description                                                 |\n| -------------- | ---------------------------------------------------- | ----------------------------------------------------------- |\n| `--root`       | `.` _(current directory)_                            | Directory in which we recursively check matching files.     |\n| `-i --include` | `*.*` _(all files)_                                  | A glob pattern that files have to match.                    |\n| `-r --regex`   | _see [here](https://gist.github.com/gruber/8891611)_ | Regex to extract URLs with group syntax support.            |\n| `--skip-ssl`   |                                                      | Do not verify the SSL certificate when performing requests. |\n| `--only-fails` |                                                      | Only output failed requests.                                |\n\n## Development\n\nInstall [Poetry](https://python-poetry.org/) and setup your environment.\n\n    poetry install\n    poetry shell\n\nRun tests with `pytest`.\n\n    poetry run pytest\n',
    'author': 'Mario Kahlhofer',
    'author_email': 'mario.kahlhofer@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/blu3r4y/pyforever',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
