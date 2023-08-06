# poshdate

![GitHub](https://img.shields.io/github/license/aj-white/poshdate)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


Poshdate is a python package that creates ordinal dates from python `datetime` and `date` objects:

`1st June 2021`

`23rd May 1990`

It is extremely lightweight having no dependencies.

---

## Getting Started

### Installation

Poshdate can be installed using `pip`

```shell
python -m pip install poshdate
```

It is recommended to use a virtual environment for your project.

### Usage

Poshdate requries the standard library `datetime` package.

```python
from datetime import datetime
import poshdate

example_date = datetime(2021, 4, 21)
print(poshdate.from_datetime(example_date)) # 21st April 2021
```

### Another date module ??

#### Intended Audience

Poshdate provides a human readable date in the ordinal format.
This is intended to be of use in report and document generation where
an approximation of a handwritten style of date is seen as nicer and a bit classier.
In other words

`21st January 2020` looks better on the page than `21 January 2020` or `21/01/2020`

#### What about existing packages ?

The python standard library `datetime` module provides many useful string formatting options via the `.strftime()` method. However, it does not provide an option to create ordinal style dates out of the box.

There are several other packages that do provide functionality to create ordinal style dates.
- [pendulum](https://github.com/sdispater/pendulum)
- [arrow](https://github.com/arrow-py/arrow)

However, these provide a lot of extra functionality that may well be beyond the needs of a user requiring a simple ordinal style date, in addition to having several additional dependancies.