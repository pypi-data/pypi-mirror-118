# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['struct_model']

package_data = \
{'': ['*']}

install_requires = \
['ujson>=4.1.0,<5.0.0']

setup_kwargs = {
    'name': 'struct-model-python',
    'version': '0.1.0',
    'description': 'Struct to model (dataclass) for python',
    'long_description': '# Welcome\n\nStruct-Model - is an annotations based wrapper for python\'s built-in `Struct` module.\n\n```python example.py\nfrom struct_model import StructModel, String, uInt4\n\nclass Form(StructModel):\n    username: String(16)\n    balance: uInt4\n    \nprint(Form("Adam Bright", 12).pack())\n# b\'Adam Bright\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x0c\'\nprint(Form.unpack(b\'Adam Bright\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x0c\').json())\n# {"username": "Adam Bright", "balance": 12}\n```\n\n',
    'author': 'Bogdan Parfenov',
    'author_email': 'adam.brian.bright@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://adambrianbright.github.io/struct-model-python/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10.0rc1,<4.0',
}


setup(**setup_kwargs)
