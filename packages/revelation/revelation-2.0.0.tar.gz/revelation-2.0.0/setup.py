# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['revelation']

package_data = \
{'': ['*'], 'revelation': ['templates/*']}

install_requires = \
['Jinja2>=3.0.1,<4.0.0',
 'Werkzeug[watchdog]>=2.0.1,<3.0.0',
 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['revelation = revelation.cli:cli',
                     'rv = revelation.cli:cli']}

setup_kwargs = {
    'name': 'revelation',
    'version': '2.0.0',
    'description': 'Make awesome reveal.js presentations with revelation',
    'long_description': "# Revelation\n\n[![PyPI](https://img.shields.io/pypi/v/revelation.svg)](https://pypi.org/project/revelation/)\n[![PyPI - License](https://img.shields.io/pypi/l/revelation.svg)](https://pypi.org/project/revelation/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/revelation.svg)](https://pypi.org/project/revelation/)\n[![Actions Status](https://github.com/humrochagf/revelation/workflows/CI/badge.svg)](https://github.com/humrochagf/revelation/actions)\n[![Coverage Status](https://coveralls.io/repos/github/humrochagf/revelation/badge.svg?branch=main)](https://coveralls.io/github/humrochagf/revelation?branch=main)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\n[revelation](https://github.com/humrochagf/revelation) is a cli tool that makes your [revealjs](https://github.com/hakimel/reveal.js) presentations nice and easy using markdown and serving it locally.\n\n## Features\n\n- Presentation server to run it locally when you are offline.\n- Presentation creation from template with a single command.\n- Custom theming support with css.\n- Export to static html tool.\n- Debug mode with server auto refresh.\n\n## Installation\n\nYou can install it with:\n\n```shell\npip install revelation\n```\n\nOr with [pipx](https://pypa.github.io/pipx/):\n\n```shell\npipx install revelation\n```\n\n## Usage\n\n### Install/Update revealjs files\n\nRevelation depends on revealjs to run its presentation and every command bellow will check and install it if revealjs isn't installed yet.\n\nBut, you can also manually install or even update it to a different version with the `installreveal` command:\n\n```shell\nrevelation installreveal\n```\n\n### Creating a new Presentation\n\nTo create a new presentation you can use `mkpresentation` command that will setup a new presentation using the base layout for you:\n\n```shell\nrevelation mkpresentation mypresentation\n```\n\n### Running the Presentation\n\nYou can start presenting with the `start` command on your presentation markdown file:\n\n```shell\ncd mypresentation\nrevelation start slides.md\n```\n\n### Static Export\n\nTo export the presentation as static HTML content use the command:\n\n```shell\nrevelation mkstatic slides.md\n```\n\n### PDF Export\n\nPresentations can be exported to PDF via a special print stylesheet. This feature will be described using [Google Chrome](https://google.com/chrome) or [Chromium](https://www.chromium.org/Home), but I got the same results using [Firefox](https://www.mozilla.org/en-US/firefox/new/).\n\n1. Run the presentation with revelation.\n2. Open your browser with the `print-pdf` as query string like : `localhost:5000/?print-pdf`.\n3. Open the in-browser print dialog (CTRL+P or CMD+P).\n4. Change the **Destination** setting to **Save as PDF**.\n5. Change the **Layout** to **Landscape**.\n6. Change the **Margins** to **None**.\n7. Enable the **Background graphics** option.\n8. Click **Save**.\n\nAlternatively you can use the [decktape](https://github.com/astefanutti/decktape) project.\n\n## Presentation Setup\n\nThe base presentation file structure looks like this:\n\n```\npresentation/\n|- media/\n|- theme/\n|- config.py\n|- slides.md\n```\n\n### The slides.md File\n\nThis is your presentation file written using markdown with some especial tags described on [markdown section](#markdown) and is placed on your presentation root folder.\n\nSplit your slides by setting up a *slide separator* and *vertical slide separator* into **REVEAL_CONFIG**. Default separator are `---` and `---~`.\n\n### The media folder\n\nBy default, revelation looks for a folder called **media** inside your presentation root folder. All media placed inside it can be referenced on your presentation by the path `/media`:\n\n```md\n![Python Logo](media/python.png)\n```\n\nYou can define a custom media path using the `--media` option on revelation `start` command.\n\n### The theme folder\n\nYou can create your custom theme file and place it inside a **theme** folder and reference it at the configuration file by the option `--theme`.\n\n### The config.py File\n\nThe configuration file located in the root folder of your presentation, allows you to customize your presentation. This file is optional and have the following configuration options:\n\n- **REVEAL_META**: Metadata of your presentation, mostly to identify the author and title.\n- **REVEAL_THEME**: A string where you can select the theme you would like to use. All revealjs base themes are available.\n- **REVEAL_CONFIG**: A python dictionary with the [revealjs configuration attributes](https://revealjs.com/config/) but using python types (e.g.: true is python boolean True)\n\nOnce you create a new presentation, all configuration values will be there for you to customize.\n\n## Markdown\n\nThe markdown used on the presentation files support everything that [revealjs docs](https://revealjs.com/markdown/) allows to place inside the `data-template` section.\n",
    'author': 'Humberto Rocha',
    'author_email': 'humrochagf@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
