# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jsqlib', 'jsqlib.helpers']

package_data = \
{'': ['*']}

install_requires = \
['python-box>=5.4,<6.0', 'sqlfluff>=0.6,<0.7']

setup_kwargs = {
    'name': 'jsqlib',
    'version': '0.3a0',
    'description': 'JSON to SQL query generator',
    'long_description': '# jsqlib\n> JSON to SQL query generator.\n\n[![pipeline status](https://gitlab.com/ru-r5/jsqlib/badges/master/pipeline.svg)](https://gitlab.com/ru-r5/jsqlib/-/commits/master)\n[![PyPI version](https://badge.fury.io/py/jsqlib.png)](https://badge.fury.io/py/jsqlib)\n\nBuilds SQL queries from pre-designed JSON structures.\n\n![](jsqlib.png)\n\n## Installation\n\nOS X & Linux & Windows:\n\n```sh\npip install jsqlib\n```\n\n## Usage example\n\n```python\nfrom jsqlib import Query\n\njson = """{\n  "query": {\n    "select": [\n      {\n        "eval": 1\n      }\n    ]\n  }\n}\n"""\n\nsql = Query(json).sql\nassert sql == \'select 1\'\n```\n\n## Development setup\n- coverage\n\n```sh\n$ pytest --cov\n```\n\n- format\n\n```sh\n$ black jsqlib -S\n```\n\n- lint\n\n```sh\n$ flakehell lint\n```\n\n## Release History\n- 0.3a0\n  - `delete` `using`, `not like` constructs\n- 0.2a0\n  - dialect based stringification\n- 0.1a0\n  - initial alpha-release\n- 0.0.1\n  - wip\n\n## Meta\n\npymancer@gmail.com (polyanalitika.ru)  \n[https://gitlab.com/ru-r5/jsqlib](https://gitlab.com/ru-r5/jsqlib)\n\n## License\n\nThis Source Code Form is subject to the terms of the Mozilla Public  \nLicense, v. 2.0. If a copy of the MPL was not distributed with this  \nfile, You can obtain one at https://mozilla.org/MPL/2.0/.  \n\n## Contributing\n\n1. Fork it (<https://gitlab.com/ru-r5/jsqlib/fork>)\n2. Create your feature branch (`git checkout -b feature/foo`)\n3. Commit your changes (`git commit -am \'Add some foo\'`)\n4. Push to the branch (`git push origin feature/foo`)\n5. Create a new Pull Request\n',
    'author': 'pymancer',
    'author_email': 'pymancer@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/ru-r5/jsqlib',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
