# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['depoverflow']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2,<3', 'toml>=0.10,<0.11']

entry_points = \
{'console_scripts': ['depoverflow = depoverflow.main:main'],
 'depoverflow.items': ['github-issue = depoverflow.github:GithubIssue',
                       'github-pr = depoverflow.github:GithubPullRequest',
                       'stackexchange-answer = '
                       'depoverflow.stackexchange:StackExchangeAnswer',
                       'stackexchange-question = '
                       'depoverflow.stackexchange:StackExchangeQuestion']}

setup_kwargs = {
    'name': 'depoverflow',
    'version': '0.1.0',
    'description': 'Watches StackOverflow answers and GitHub issues referenced in code for changes',
    'long_description': 'Depoverflow\n-----------\n\nThis tool checks your source code for references to Stackoverflow answers and GitHub issues and warns you if those change.\n\nWhy?\n----\n\nThere are plenty of tools that will let you know if your package dependencies have changed (`poetry show -o`, `npm outdated`, ...). There are even cloud-based services like Dependabot.\n\nHowever, if you copy/paste code from Stackoverflow answers or GitHub issues, you will never be notified of updates.\n\nFeatures\n--------\n\n* Find references to Stackoverflow answers and questions in code comments, to alert of edits and/or comments\n* Find references to GitHub issues in code comments, to alert of open and close events and/or comments\n* Optionally supports specific keywords such as "Works around"\n* Saves current status of referenced items in a TOML file (similar to a lockfile), that you can check into version control (or not)\n\nHow to use\n----------\n\nInstall the tool: `pip install depoverflow`\n\nCreate a configuration file `depoverflow.toml` with the list of source file patterns you want to read (in [Python glob format](https://docs.python.org/3/library/pathlib.html#pathlib.Path.glob)):\n\n```toml\nsources = [\n    "src/**.py",\n    "tests.py",\n    "native/*.c",\n]\n```\n\nRun the tool: `depoverflow`.\n\nA file `depoverflow.status` will be created, which you can check into version control or not. It is a TOML file containing the current status of the items you reference from your code, so that a warning can be shown the next time they change.\n',
    'author': 'Remi Rampin',
    'author_email': 'remi@rampin.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/remram44/depoverflow',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
