# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sqlite2pg', 'sqlite2pg.modules']

package_data = \
{'': ['*']}

install_requires = \
['aiosqlite>=0.17.0,<0.18.0', 'asyncpg>=0.24.0,<0.25.0']

entry_points = \
{'console_scripts': ['sqlite2pg = sqlite2pg.cli:main']}

setup_kwargs = {
    'name': 'sqlite2pg',
    'version': '0.1.0',
    'description': 'An Sqlite3 to Postgresql database migration tool.',
    'long_description': '# sqlite2pg\n\nAn Sqlite3 to Postgresql database migration tool.\n\n## A warning\n\nThis project is still in very early development, and will not be ready until the v1.0 release.\nPlease refrain from using sqlite2pg for now.\n\n## Why sqlite2pg\n\n - An easy to use command line interface.\n - Options to accomodate different use cases.\n - Complete full migrations, or just generate schema.\n - Asynchronous, keeping performance in mind for big jobs.\n\n## Installation\n\nsqlite2pg requires python 3.8.0 or greater.\n\nTo get started:\n```bash\npip install sqlite2pg\n```\n\n## License\n\nsqlite2pg is licensed under the [BSD 3-Clause License](https://github.com/Jonxslays/sqlite2pg/blob/master/LICENSE).\n',
    'author': 'Jonxslays',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Jonxslays/sqlite2pg',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<=3.10',
}


setup(**setup_kwargs)
