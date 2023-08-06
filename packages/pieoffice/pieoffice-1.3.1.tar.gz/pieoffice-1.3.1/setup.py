# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pieoffice']

package_data = \
{'': ['*']}

install_requires = \
['betacode>=1.0,<2.0', 'docopt>=0.6.2,<0.7.0']

setup_kwargs = {
    'name': 'pieoffice',
    'version': '1.3.1',
    'description': 'A terminal based script converter for ancient (Proto-)Indo-European languages.',
    'long_description': '# PIE-Office: A terminal based script converter for ancient (Proto-)Indo-European languages.\n\nThis application is a tentative to convert my editor-based keybinding plugins for typing ancient Indo-European languages `pievim` and `pie-macs` to a standalone application.\nI am not much of a GUI person, so this comes as a terminal based converter, but it will hopefully be more useful for those not using `vim` or `emacs`.\nGenerally, this project will lag behind the `pievim`, since it is being done in a rather hobbist fashion.\n\nSo far, the mappings cover:\n - Proto-Indo-European (`pieoffice convert pie <text>`)\n - Indic:\n    - Vedic / Sanskrit:\n        - Devanagari (`pieoffice vedic convert <text>` or `pieoffice sanskrit convert <text>`)\n        - ISO (`pieoffice vedic convert <text> -t iso` or `pieoffice sanskrit convert <text> -t iso`)\n        - IAST (`pieoffice vedic convert <text> -t iast` or `pieoffice sanskrit convert <text> -t iast`)\n - Iranic:\n     - Avestan:\n         - Script (`pieoffice avestan convert <text>`)\n         - Transliterated as in Hoffman (`pieoffice convert avestan <text> -t translit`)\n     - Old Persian Cuneiform (`pieoffice convert oldpersian <text>`)\n - Celtic:\n     - Ogham Script (`pieoffice convert ogham <text>`)\n - Italic:\n     - Oscan Script (`pieoffice convert oscan <text>`)\n - Germanic:\n     - Gothic Script (`pieoffice convert gothic <text>`)\n - Armenian:\n     - Script (`pieoffice convert armenian <text>` or `pieoffice convert armenian <text> -t armenian`)\n     - Script, Maiscules only (`pieoffice convert armenian <text> -t maiscules`)\n     - Romanized in ISO (`pieoffice convert armenian <text> -t iso`)\n     - Romanized in Classical (`pieoffice convert armenian <text> -t maiscules`)\n - Greek:\n    - Polytonic Greek (`pieoffice convert greek <text>`)\n    - Mycenaean Linear B Script (`pieoffice convert linearb <text>`)\n    - Cypriot Syllabary (`pieoffice convert cypriot <text>`)\n - Anatolian:\n    - Hieroglyphic Luwian (`pieoffice convert luwian <text>`)\n    - Lydian (`pieoffice convert lydian <text>`)\n    - Lycian (`pieoffice convert lycian <text>`)\n    - Carian (`pieoffice convert carian <text>`)\n\n# Installation\n\nThe easiest way so far is, if you have pip, to run:\n\n```bash\npip install --user pieoffice\n```\n\nAnd to upgrade:\n\n```bash\npip install --upgrade pieoffice\n```\n\n# Usage\n\nTo figure out what are the languages available:\n\n```bash\npieoffice list\n```\n\nTo check the rules for a given language:\n\n```bash\npieoffice rules <language>\n```\n\nTo convert:\n\n```bash\npieoffice convert <language> <text>\n```\n\n# TODO\n\n## JSON\n\nIt could be better having the dictionary structures converted to json, since it would allow some fancier techniques, maybe?\n\n# Contribute\n\nThis is a hobbist project, so please let me know if you would employ a different algorithm or make a pull request.\nAny tinkering with the code is most welcome.\n\n',
    'author': 'Caio Geraldes',
    'author_email': 'caio.geraldes@usp.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
