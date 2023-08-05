# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['podping_hivewriter',
 'podping_hivewriter.cli',
 'podping_hivewriter.config',
 'podping_hivewriter.models']

package_data = \
{'': ['*']}

install_requires = \
['asgiref>=3.4,<4.0',
 'beem>=0.24,<0.25',
 'cffi>=1.14.5,<2.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'pyzmq>=22.1.0,<23.0.0',
 'rfc3987>=1.3.8,<2.0.0',
 'single-source>=0.2.0,<0.3.0',
 'typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['podping = podping_hivewriter.cli.podping:app']}

setup_kwargs = {
    'name': 'podping-hivewriter',
    'version': '1.0.0a0',
    'description': '',
    'long_description': '# podping-hivewriter\nThe Hive writer component of podping.\n\n## Linux CLI Install\n\n### Using [pipx](https://pypa.github.io/pipx/) (preferred over pip)\n```shell\npipx install podping-hivewriter\n```\n\n### Using pip\n```shell\npip install --user podping-hivewriter\n```\n\nMake sure you have `~/.local/bin/` on your `PATH`.\n\nSee the dedicated [CLI docs](cli.md) for more information.\n\n## Container\n\n## docker-compose\n\nTODO\n\n### Building the image with Docker\n\nLocally build the podping-hivewriter container with a "develop" tag\n\n```shell\ndocker build -t podpinghivewriter:develop .\n```\n\n\n### Running the image\n\nRun the locally built image in a container, passing local port 9999 to port 9999 in the container.\nENV variables can be passed to docker with `--env-file` option after modifying the `.env.EXAMPLE` file and renaming it to `.env`\n\n```shell\ndocker run --rm -p 9999:9999 --env-file .env --name podping podpinghivewriter:develop\n```\n\nRunning with command line options, like `--dry-run` for example, add them with the full podping command.\nSettings can also be passed with the `-e` option for Docker.  Note, we leave out `-p 9999:9999` here because we\'re not running the server.\n\n```shell\ndocker run --rm \\\n    -e PODPING_HIVE_ACCOUNT=<account> \\\n    -e PODPING_HIVE_POSTING_KEY=<posting-key> \\\n    podpinghivewriter:develop \\\n    podping --dry-run write https://www.example.com/feed.xml\n```\n\nSee the [CLI docs](cli.md) for default values.\n\n## Development\n\nWe use [poetry](https://python-poetry.org/) for dependency management.  Once you have it, clone this repo and run:\n\n```shell\npoetry install\n```\n\nThen to switch to the virtual environment, use:\n\n```shell\npoetry shell\n```\n\nAfter that you should be able to run the `podping` command or run the tests:\n\n```shell\npytest\n```\n\nTo run all tests, make sure to set the necessary environment variables for your Hive account.  This can take many minutes:\n\n```shell\npytest --runslow\n```\n',
    'author': 'Brian of London',
    'author_email': 'brian@podping.org',
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
