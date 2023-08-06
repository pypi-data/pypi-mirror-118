# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sdgs',
 'sdgs.auth',
 'sdgs.model',
 'sdgs.survey_individu',
 'sdgs.survey_individu.tambah']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=21.2.0,<22.0.0',
 'beautifulsoup4>=4.9.3,<5.0.0',
 'cattrs>=1.8.0,<2.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'requests>=2.26.0,<3.0.0',
 'ujson>=4.0.2,<5.0.0']

setup_kwargs = {
    'name': 'sdgs-dashboard',
    'version': '0.2.0',
    'description': ' Modul python untuk dashboard sdgs kemendesa.',
    'long_description': '# sdgs-dashboard\n\n[![sdgs-dashboard - PyPi](https://img.shields.io/pypi/v/sdgs-dashboard)](https://pypi.org/project/sdgs-dashboard/)\n[![Supported Python versions](https://img.shields.io/pypi/pyversions/sdgs-dashboard)](https://pypi.org/project/sdgs-dashboard/)\n[![Donate Saweria](https://img.shields.io/badge/Donasi-Saweria-blue)](https://saweria.co/hexatester)\n[![LISENSI](https://img.shields.io/github/license/hexatester/sdgs-dashboard)](https://github.com/hexatester/sdgs-dashboard/blob/main/LICENSE)\n\nModul python untuk dashboard sdgs kemendesa.\n',
    'author': 'hexatester',
    'author_email': 'hexatester@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hexatester/sdgs-dashboard',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.10,<4.0.0',
}


setup(**setup_kwargs)
