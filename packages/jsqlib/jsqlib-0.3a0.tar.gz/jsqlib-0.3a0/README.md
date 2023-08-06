# jsqlib
> JSON to SQL query generator.

[![pipeline status](https://gitlab.com/ru-r5/jsqlib/badges/master/pipeline.svg)](https://gitlab.com/ru-r5/jsqlib/-/commits/master)
[![PyPI version](https://badge.fury.io/py/jsqlib.png)](https://badge.fury.io/py/jsqlib)

Builds SQL queries from pre-designed JSON structures.

![](jsqlib.png)

## Installation

OS X & Linux & Windows:

```sh
pip install jsqlib
```

## Usage example

```python
from jsqlib import Query

json = """{
  "query": {
    "select": [
      {
        "eval": 1
      }
    ]
  }
}
"""

sql = Query(json).sql
assert sql == 'select 1'
```

## Development setup
- coverage

```sh
$ pytest --cov
```

- format

```sh
$ black jsqlib -S
```

- lint

```sh
$ flakehell lint
```

## Release History
- 0.3a0
  - `delete` `using`, `not like` constructs
- 0.2a0
  - dialect based stringification
- 0.1a0
  - initial alpha-release
- 0.0.1
  - wip

## Meta

pymancer@gmail.com (polyanalitika.ru)  
[https://gitlab.com/ru-r5/jsqlib](https://gitlab.com/ru-r5/jsqlib)

## License

This Source Code Form is subject to the terms of the Mozilla Public  
License, v. 2.0. If a copy of the MPL was not distributed with this  
file, You can obtain one at https://mozilla.org/MPL/2.0/.  

## Contributing

1. Fork it (<https://gitlab.com/ru-r5/jsqlib/fork>)
2. Create your feature branch (`git checkout -b feature/foo`)
3. Commit your changes (`git commit -am 'Add some foo'`)
4. Push to the branch (`git push origin feature/foo`)
5. Create a new Pull Request
