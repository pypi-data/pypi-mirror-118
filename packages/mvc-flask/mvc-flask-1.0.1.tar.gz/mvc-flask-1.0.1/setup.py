# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mvc_flask']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=2.0.1,<2.1.0']

setup_kwargs = {
    'name': 'mvc-flask',
    'version': '1.0.1',
    'description': 'turn standard flask into mvc',
    'long_description': '![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/marcuxyz/mvc_flask) ![GitHub Workflow Status](https://img.shields.io/github/workflow/status/marcuxyz/mvc_flask/unit%20test) ![GitHub](https://img.shields.io/github/license/marcuxyz/mvc_flask) ![PyPI - Downloads](https://img.shields.io/pypi/dm/mvc_flask) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mvc_flask) ![PyPI](https://img.shields.io/pypi/v/mvc_flask)\n\nYou can use the mvc pattern in your flask application using this extension.\n\n# Installation\n\nRun the follow command to install `mvc_flask`:\n\n```shell\n$ pip install mvc_flask\n```\n\n# Configuration\n\nTo configure the `mvc_flask` you need import and register in your application:\n\n\n```python\nfrom mvc_flask import FlaskMVC\nmvc = FlaskMVC()\n```\n\nOr use factory function\n\n```python\nmvc = FlaskMVC()\n\ndef create_app():\n  ...\n  mvc.init_app(app)\n```\n\nBy default the `mvc_flask` assumes that your application directory will be `app`, but, you can change it. Passing the object of configuration:\n\n```python\napp.config["FLASK_MVC_DIR"] = "sample_app"\n```\n\n# Create MVC Pattern\n\n`mvc_flask` assumes that your application will have these characteristics: \n\n```text\napp\n├── __ini__.py\n├── controllers\n│   ├── contact_controller.py\n│   └── home_controller.py\n├── model\n├── routes.json\n└── views\n    ├── index.html\n    └── post\n        └── new.html\n```\n\nThe routes will be something as:\n\n```json\n[\n  {\n    "method": "GET",\n    "path": "/",\n    "controller": "home",\n    "action": "index"\n  },\n  {\n    "method": "get",\n    "path": "/new",\n    "controller": "home",\n    "action": "new"\n  },\n  {\n    "method": "post",\n    "path": "/create",\n    "controller": "home",\n    "action": "create"\n  },\n  {\n    "method": "GET",\n    "path": "/contact",\n    "controller": "contact",\n    "action": "index"\n  }\n]\n```\n\n# Tests\n\nYou can run the tests, executing the follow command:\n\n```shell\n$ make test\n```\n\n![](/prints/test_runner.png)\n',
    'author': 'Marcus Pereira',
    'author_email': 'oi@negros.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/marcuxyz/mvc_flask',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
