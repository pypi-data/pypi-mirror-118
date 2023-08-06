# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['commanderbot',
 'commanderbot.core',
 'commanderbot.ext',
 'commanderbot.ext.automod',
 'commanderbot.ext.automod.actions',
 'commanderbot.ext.automod.actions.abc',
 'commanderbot.ext.automod.conditions',
 'commanderbot.ext.automod.conditions.abc',
 'commanderbot.ext.automod.events',
 'commanderbot.ext.automod.triggers',
 'commanderbot.ext.faq',
 'commanderbot.ext.help_chat',
 'commanderbot.ext.help_chat.sql_store',
 'commanderbot.ext.invite',
 'commanderbot.ext.jira',
 'commanderbot.ext.kick',
 'commanderbot.ext.manifest',
 'commanderbot.ext.pack',
 'commanderbot.ext.ping',
 'commanderbot.ext.poster_board',
 'commanderbot.ext.quote',
 'commanderbot.ext.roles',
 'commanderbot.ext.stacktracer',
 'commanderbot.ext.status',
 'commanderbot.ext.vote',
 'commanderbot.lib',
 'commanderbot.lib.guards',
 'commanderbot.lib.utils']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'SQLAlchemy>=1.4,<1.4.23',
 'aiohttp>=3.7.4,<4.0.0',
 'aiosqlite>=0.17.0,<0.18.0',
 'beet>=0.36.0',
 'colorama>=0.4.3,<0.5.0',
 'colorlog>=4.2.1,<5.0.0',
 'emoji>=1.4.2,<2.0.0',
 'lectern>=0.15.0',
 'typing-extensions==3.10.0.0']

extras_require = \
{':python_version >= "3.10" and python_version < "3.11"': ['numpy>=1.21,<2.0']}

setup_kwargs = {
    'name': 'commanderbot',
    'version': '0.17.0',
    'description': 'A collection of utilities and extensions for discord.py bots.',
    'long_description': '# commanderbot-py\n\nA collection of utilities and extensions for discord.py bots.\n\n[![package-badge]](https://pypi.python.org/pypi/commanderbot/)\n[![version-badge]](https://pypi.python.org/pypi/commanderbot/)\n\n## Requirements\n\n- Python 3.10+\n- discord.py 2.0+\n\n## Running your bot\n\nYou can run your own bot without writing any code.\n\nYou will need the following:\n\n1. Your own [Discord Application](https://discordapp.com/developers/applications) with a bot token.\n2. A [configuration file](#configuring-your-bot) for the bot.\n3. A Python 3.10+ environment.\n   - It is recommended to use a [virtual environment](https://docs.python.org/3/tutorial/venv.html) for this.\n   - You can use [pyenv](https://github.com/pyenv/pyenv) to build and run Python 3.10.\n4. If you have [poetry](https://python-poetry.org/), you can `poetry install` instead of using `pip`. (Just make sure that dev dependencies are also installed.) Otherwise, you need to install a few packages with `pip`:\n   - Run `pip install commanderbot` to install the bot core package.\n   - Run `pip install git+https://github.com/Rapptz/discord.py.git@848d752` to install the latest (and final) version of the discord.py 2.0 beta from GitHub.\n   - Run `pip install git+https://github.com/vberlier/nbtlib@main` to install the latest version of nbtlib from GitHub.\n\nThe first thing you should do is check the CLI help menu:\n\n```bash\npython -m commanderbot --help\n```\n\nThere are three ways to provide your bot token:\n\n1. (Recommended) As the `BOT_TOKEN` environment variable: `BOT_TOKEN=put_your_bot_token_here`\n2. As a CLI option: `--token put_your_bot_token_here`\n3. Manually, when prompted during start-up\n\nHere\'s an example that provides the bot token as an argument:\n\n```bash\npython -m commanderbot bot.json --token put_your_bot_token_here\n```\n\n## Configuring your bot\n\nThe current set of configuration options is limited. Following is an example configuration that sets the command prefix and loads the `status` and `faq` extensions.\n\n> Note that with this configuration, the `faq` extension will require read-write access to `faq.json` in the working directory.\n\n```json\n{\n  "command_prefix": ">",\n  "extensions": [\n    "commanderbot.ext.status",\n    {\n      "name": "commanderbot.ext.faq",\n      "enabled": true,\n      "options": {\n        "database": "faq.json",\n        "prefix": "?"\n      }\n    }\n  ]\n}\n```\n\n[package-badge]: https://img.shields.io/pypi/v/commanderbot.svg\n[version-badge]: https://img.shields.io/pypi/pyversions/commanderbot.svg\n',
    'author': 'Arcensoth',
    'author_email': 'arcensoth@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/CommanderBot-Dev/commanderbot-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
