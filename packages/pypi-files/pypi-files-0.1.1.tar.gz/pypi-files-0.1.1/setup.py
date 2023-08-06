# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pypi_files']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0', 'fire>=0.4.0,<0.5.0', 'requests>=2.26.0,<3.0.0']

entry_points = \
{'console_scripts': ['pf = pypi_files:main']}

setup_kwargs = {
    'name': 'pypi-files',
    'version': '0.1.1',
    'description': 'Check and download package source files from PyPI.',
    'long_description': '# pypi-files\n[![pytest](https://github.com/rcmdnk/pypi-files/actions/workflows/test.yml/badge.svg)](https://github.com/rcmdnk/pypi-files/actions/workflows/test.yml)\n\nCheck and download package source files from PyPI.\n\n\n# Rqeuirement\n\n* Python: tested with 3.6 or later\n\n# Install\n\n    $ pip install pypi-files\n\n# Usage\n\n    Usage: pf <command> [--package <pacakge>] [--version <version>] [--file <yaml file>] [--destination <destination>]\n\n    command:\n      get_file_list    Show package source file URLs.\n      download         Download package source files.\n\nTo get package source files, use `pf get_file_list`:\n\n    pf get_file_list [--package <pacakge>] [--version <version>] [--file <yaml file>]\n\nYou can give a package name by `--pacakge` and give a version as an option.\nIf `--version` is not passed, the latest version will be used.\n\n    $ pf get_file_list --package pandas --version 1.3.2\n    https://files.pythonhosted.org/packages/cf/f7/6c0dd488b5f5f1c0c1a48637df45046334d0be684faaf3536429f14aa9de/pandas-1.3.2.tar.gz\n\nYou can also use YAML file with a package list.\n\nThe file should be a list of dictionaries (`<package>: <version>`) like:\n\n    ---\n    - pandas: 1.3.2\n    - numpy: latest\n    - numpy: 1.21.0\n\nIf you want the latest version, use `latest`.\n\n    $ pf get_file_list --files ./packages.yml\n    https://files.pythonhosted.org/packages/cf/f7/6c0dd488b5f5f1c0c1a48637df45046334d0be684faaf3536429f14aa9de/pandas-1.3.2.tar.gz\n    https://files.pythonhosted.org/packages/3a/be/650f9c091ef71cb01d735775d554e068752d3ff63d7943b26316dc401749/numpy-1.21.2.zip\n    https://files.pythonhosted.org/packages/66/03/818876390c7ff4484d5a05398a618cfdaf0a2b9abb3a7c7ccd59fe181008/numpy-1.21.0.zip\n\nTo download package source files, use `download`.\nYou can set output destination by `--destination`.\n\n    pf download [--package <pacakge>] [--version <version>] [--file <yaml file>] [--destination <destination>]\n\nThe default destination is current directory (`./`).\n\n    $ pf download --package pandas --version 1.3.2\n    Downloading https://files.pythonhosted.org/packages/cf/f7/6c0dd488b5f5f1c0c1a48637df45046334d0be684faaf3536429f14aa9de/pandas-1.3.2.tar.gz to ./pandas-1.3.2.tar.gz...\n    $ ls\n    pandas-1.3.2.tar.gz\n',
    'author': 'rcmdnk',
    'author_email': 'rcmdnk@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rcmdnk/pypi-files',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
