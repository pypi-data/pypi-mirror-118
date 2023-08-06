# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyscora_wrangler', 'pyscora_wrangler.aws']

package_data = \
{'': ['*']}

install_requires = \
['awswrangler>=2.10.0,<3.0.0',
 'boto3>=1.17.70,<2.0.0',
 'fastparquet>=0.5.0,<0.6.0',
 'numpy>=1.20.2,<2.0.0',
 'pandas>=1.2.3,<2.0.0',
 'pyarrow>=3.0.0,<4.0.0',
 'pyathena>=2.3.0,<3.0.0',
 'smart-open[all]>=5.1.0,<6.0.0']

setup_kwargs = {
    'name': 'pyscora-wrangler',
    'version': '0.1.0',
    'description': 'Wrappers for Data Engineer tasks.',
    'long_description': '# Pyscora-Wrangler\n\nPython package that consists mainly of wrappers for Data Engineering tasks.\n\n# Installing\n\nIf the user has the Poetry package management, the package can locally be\ninstalled with the command: \n\n```bash\npoetry install\n```\n\nYou can also build it with the command and install it through pip or Poetry:\n\n```bash\npoetry build\n```\n',
    'author': 'Adriel Martins',
    'author_email': 'adriel.martins@oncase.com.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/oncase/pyscora-wrangler/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
