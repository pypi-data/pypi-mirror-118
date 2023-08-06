# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nv', 'nv.nfe']

package_data = \
{'': ['*']}

install_requires = \
['dicttoxml>=1.7.4,<2.0.0',
 'nv-utils>=0.2.0a2,<0.3.0',
 'xmltodict>=0.12.0,<0.13.0']

setup_kwargs = {
    'name': 'nv-nfe',
    'version': '0.1.0a1',
    'description': 'Simple XML parser for reading standard Brazilian digital invoices (NFe)',
    'long_description': '# nv.nfe\nSimple XML parser for reading standard Brazilian digital invoices (NFe)\n\n## Disclaimers\nThis library is a "quick and dirt" reader for Brazilian NFe (Nota Fiscal Eletrônica).  The package itself is based on \na simple xml serializer and parser built on top of xmltodict.  **This has NOT been\ntested under for xml vulnerabilities** and will probably never will, as it was develped as an internal parser for data analysis.\n\n\n## Disclaimers\nTHIS IS UNDOCUMENTED WORK IN PROGRESS. READ THE LICENSE AND USE IT AT YOUR OWN RISK.\n\nTHIS IS AN ALPHA AND BREAKING CHANGES MAY (AND PROBABLY WILL) OCCUR.\n',
    'author': 'Gustavo Santos',
    'author_email': 'gustavo@next.ventures',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gstos/nv-nfe',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
