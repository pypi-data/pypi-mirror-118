# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['timespeaker']

package_data = \
{'': ['*']}

install_requires = \
['gtts>=2.1.1,<3.0.0', 'pyttsx3>=2.90,<3.0']

entry_points = \
{'console_scripts': ['timespeaker = timespeaker.main:cli']}

setup_kwargs = {
    'name': 'timespeaker',
    'version': '0.1.3',
    'description': 'Announce the time every hour similar to Mac OS X. Say the Time using Google TTS or espeak.',
    'long_description': "# TimeSpeaker\n\nAnnounce the time every hour similar to Mac OS X. Say the Time using Google TTS or espeak.\n\n# Requirements\n\n- python3.6+\n- playsound\n- gtts or pyttsx3\n\nFor development\n\n- poetry \n- flake8\n- black\n- pytest\n\n# TODO\n\n- Use python: [threading.Timer](https://docs.python.org/3/library/threading.html?highlight=timer#threading.Timer)\n- Create tests\n- Add system tray (opcional) by cli\n- Update/Fix to PyPi (`pip install timespeaker`)\n- Move Makefile to Parent\n- Configure PULL_REQUESTS AND ISSUES template\n- Configure lint\n- Configure github actions (or circleci)\n- Test i3 configs\n- Add support to Cron\n- Use a global DEBUG\n- When merge to `main` build and publish to PyPi (github actions)\n\n# Install\n\n## Default (Working In Progress)\n\n```bash\npip install timespeaker\n```\n\n## Local\n\n### On Local User\n\n```bash\n# pyenv shell +3.6.0\n# asdf shell python +3.6.0\n\n# optional (poetry create a virtualenv for you)\npython -m venv .venv \n\n# install dependencies\nmake install\n\n# clean old builds\nmake clean\n\n# build package\nmake build\n\n# install on local user package (python)\npip install --user dist/{path_from_last_command}.whl\n```\n\n**Test local install**\n```bash\ntimespeaker check --speaker gtts\n```\n\n# Configure\n\n## AutoStart (Working In Progress)\n\n```bash\nmake configure-autostart\n```\n\n## i3 (Working In Progress)\n\n```bash\nmake configure-i3\n```\n\n## Cron (Working In Progress)\n\nComing Soon\n\n```bash\nsudo make configure-cron\n```\n\n## Systemd (Working In Progress)\n\n```bash\nsudo make configure-systemd\n```\n\n## Remove configurations\n\n```bash\n# Systemd\nsudo make remove-systemd\n\n# Autostart\nmake remove-autostart\n\n# i3\n# coming soon\n\n# Cron\n# coming soon\n```\n\n# Usage\n\nDefault usage using gtts to speak and saving in `/tmp/timespeaker/`\n\n```bash\n# after make install (or poetry install)\npoetry run timespeaker start\n\n# OR if configured (local user or via pip install timespeaker)\ntimespeaker start\n```\n\nCustom command:\n\n```bash\npoetry run timespeaker start --speaker=pyttsx3 --player=vlc --path-folder=/tmp/timespeaker/\n```\n\n# Development\n\nUsing virtualenv (python venv):\n\n```bash\n# create virtualenv\n# virtualenv .venv [-p /path/to/python3.6+] # require virtualenv\npython -m venv .venv\n\n# Enter virtualenv\nsource .venv/bin/activate\n\n# to exit of virtual env run \ndeactivate\n```\n\nDev install (poetry required)\n\n```bash\npoetry install\n```\n\nSee more commands with\n\n```bash\nmake help\n```\n\n# Tests\n\n```bash\nmake test\n```\n\n# License\n\nMIT LICENSE\n\n# Contributing\n\nI encourage you to contribute to this project! Join us!\n\nTrying to report a possible security vulnerability? [Open a issue now](https://github.com/wallacesilva/timespeaker/issues/new)\n\nEveryone interacting in this project and its sub-projects' codebases, issue trackers, chat rooms, and mailing lists is expected to follow the code of conduct (building, but respect everyone).\n",
    'author': 'Wallace Silva',
    'author_email': 'contact@wallacesilva.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/wallacesilva/timespeaker/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
