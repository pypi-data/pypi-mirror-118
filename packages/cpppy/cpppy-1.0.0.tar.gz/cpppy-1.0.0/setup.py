# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'lib'}

modules = \
['cpp']
setup_kwargs = {
    'name': 'cpppy',
    'version': '1.0.0',
    'description': 'Implementing C++ Semantics in Python',
    'long_description': '# cpp.py\n\nImplementing C++ Semantics in Python\n\n## Disclaimer\n\nThis project is an experiment.\n\nPlease don\'t use it in any sensitive context.\n\n## Installation\n\n### From PyPI\n\n```shell\npip install cpppy\n```\n\n### From Source (Dev)\n\n```shell\ngit clone https://github.com/tmr232/cpppy.git\ncd cpppy\npoetry install\npoetry shell\n```\n\n## Usage & Examples\n\nImport `magic` inside a module and watch the magic happen.\n\nNote that it only works inside modules.\nImporting it in an interactive shell or a Jupyter Notebook won\'t work.\n\nThat said, functions from said modules can be imported and used\nin regular Python code. \n\n```python\n# examples/greeter.py\n\nfrom cpp import magic\n\n\nclass Greeter:\n    name: str\n\n    public()\n\n    def Greeter(name):\n        this.name = name\n        print(f"Hello, {this.name}!")\n\n    def _Greeter():\n        print(f"Goodbye, {this.name}.")\n\n\ndef main():\n    greeter1 = Greeter(1)\n    greetee2 = Greeter(2)\n\n```\n\n```shell\n>>> python examples/greeter.py\nHello, 1!\nHello, 2!\nGoodbye, 2.\nGoodbye, 1.\n```\n\n## Presentations\n\n* [Implementing C++ Semantics in Python](https://github.com/tmr232/talks/tree/main/CoreCpp2021) (Core C++ 2021)',
    'author': 'Tamir Bahar',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tmr232/cpppy',
    'package_dir': package_dir,
    'py_modules': modules,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
