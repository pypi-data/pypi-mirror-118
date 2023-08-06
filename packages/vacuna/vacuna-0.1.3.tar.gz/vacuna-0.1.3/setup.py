# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vacuna']

package_data = \
{'': ['*']}

extras_require = \
{'docs': ['mkdocs>=1.2.2,<2.0.0',
          'mkdocs-material>=7.2.5,<8.0.0',
          'mkdocstrings>=0.15.2,<0.16.0']}

setup_kwargs = {
    'name': 'vacuna',
    'version': '0.1.3',
    'description': 'Reusable Lightweight Pythonic Dependency Injection Library',
    'long_description': "# Vacuna\n\n> Inject everything!\n\n![PyPI](https://img.shields.io/pypi/v/vacuna)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/vacuna)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/vacuna)\n![PyPI - License](https://img.shields.io/pypi/l/vacuna)\n[![codecov](https://codecov.io/gh/frndmg/vacuna/branch/master/graph/badge.svg?token=L38OHXFKQO)](https://codecov.io/gh/frndmg/vacuna)\n\nVacuna is a little library to provide dependency management for your python code.\n\n# Install\n\n```bash\npip install vacuna\n```\n\n# Usage\n\n```python\nimport vacuna\n\ncontainer = vacuna.Container()\n\n@container.dependency(name='app')\nclass App:\n    def run(self):\n        print('very important computation')\n\n@container.dependency()\ndef main(app):\n    app.run()\n\nif __name__ == '__main__':\n    container.run(main)\n```",
    'author': 'Fernando Martinez Gonzalez',
    'author_email': 'frndmartinezglez@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
