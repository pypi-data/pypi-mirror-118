# chopin
This repository is intended to make it easier to use the Chopin's compositions.
It does not follow any coding conventions :)

[![](https://img.shields.io/pypi/pyversions/chopin)](https://www.python.org/)
[![](https://img.shields.io/pypi/v/chopin)](https://pypi.org/project/chopin/)
[![](https://img.shields.io/github/license/ster-phys/chopin)](https://opensource.org/licenses/MIT)

## How to Install
```sh
$ pip install chopin
```

#### Requires
```sh
$ pip install requests youtube_dl bs4 lxml
```

## How to Use
- Example
```python
from chopin import Chopin

ch = Chopin(force=True, output=True, semaphore=12)
compo = ch.random_get()
compo.links[0].download("./foo.mp3")
```
