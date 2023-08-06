# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['camundactl', 'camundactl.cmd', 'camundactl.cmd.openapi', 'camundactl.output']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.0.1,<4.0.0',
 'PyYAML>=5.4.1,<6.0.0',
 'click>=8.0.1,<9.0.0',
 'jsonpath-ng>=1.5.3,<2.0.0',
 'jsonschema>=3.2.0,<4.0.0',
 'requests>=2.26.0,<3.0.0',
 'tabulate>=0.8.9,<0.9.0',
 'toolz>=0.11.1,<0.12.0',
 'types-requests>=2.25.6,<3.0.0']

entry_points = \
{'console_scripts': ['cctl = camundactl.cmd.base:root']}

setup_kwargs = {
    'name': 'camundactl',
    'version': '0.1.0a1',
    'description': 'A Camunda cli that interacts with the rest api',
    'long_description': None,
    'author': 'Jens Blawatt',
    'author_email': 'jens.blawatt@codecentric.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
