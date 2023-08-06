# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qua',
 'qua.grpc',
 'qua.grpc.io',
 'qua.grpc.io.qualang',
 'qua.grpc.io.qualang.api']

package_data = \
{'': ['*']}

install_requires = \
['betterproto>=1.2.5,<2.0.0', 'grpclib>=0.4.2,<0.5.0']

setup_kwargs = {
    'name': 'qua',
    'version': '0.1.0',
    'description': 'SDK to interact with a quantum computer at the pulse level',
    'long_description': '# QUA SDK\n\nPython SDK for QUA \n\nPulse level language for controlling a Quantum Computer\n',
    'author': 'Tal Shani',
    'author_email': 'tal@quantum-machines.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/qua-platform/qua-sdk-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
