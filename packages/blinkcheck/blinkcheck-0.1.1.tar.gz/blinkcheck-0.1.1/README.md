# 🌎 `blinkcheck` - a basic link checker

[![Latest Release](https://img.shields.io/github/release/blu3r4y/blinkcheck.svg?style=popout-square)](https://github.com/blu3r4y/blinkcheck/releases/latest)
[![PyPI Version](https://img.shields.io/pypi/v/blinkcheck?style=popout-square)](https://pypi.org/project/blinkcheck/)
[![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg?style=popout-square)](LICENSE.txt)

Check for dead links in all files, with support for regex URL extraction and glob file patterns.

## Installation

    pip install blinkcheck

## Usage Examples

Check for dead links in all files, starting in the current directory.

    blinkcheck

Check for dead links in all Markdown `*.md` files of a specific `./docs` folder.

    blinkcheck --root ./docs -i *.md

Check for dead links in LaTeX `*.tex` files in the current directory with regex `\\url{(.*?)}`.  
If a regex contains one group constructs, the group is used as the link.

    blinkcheck -i *.tex -r "\\url{(.*?)}"

Only list failed links and do not verify SSL certificates.

    blinkcheck --skip-ssl --only-fails

## Available Arguments

| Argument       | Default Value                                        | Description                                                 |
| -------------- | ---------------------------------------------------- | ----------------------------------------------------------- |
| `--root`       | `.` _(current directory)_                            | Directory in which we recursively check matching files.     |
| `-i --include` | `*.*` _(all files)_                                  | A glob pattern that files have to match.                    |
| `-r --regex`   | _see [here](https://gist.github.com/gruber/8891611)_ | Regex to extract URLs with group syntax support.            |
| `--skip-ssl`   |                                                      | Do not verify the SSL certificate when performing requests. |
| `--only-fails` |                                                      | Only output failed requests.                                |

## Development

Install [Poetry](https://python-poetry.org/) and setup your environment.

    poetry install
    poetry shell

Run tests with `pytest`.

    poetry run pytest
