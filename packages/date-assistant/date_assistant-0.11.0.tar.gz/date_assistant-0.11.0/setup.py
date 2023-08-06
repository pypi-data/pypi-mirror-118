# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['date_assistant']

package_data = \
{'': ['*']}

install_requires = \
['pre-commit>=2.15.0,<3.0.0', 'python-dateutil>=2.8.2,<3.0.0']

setup_kwargs = {
    'name': 'date-assistant',
    'version': '0.11.0',
    'description': '🗓 Classes and functions with intuitive names for common dates operations',
    'long_description': "[![Coverage Status](https://coveralls.io/repos/github/jalvaradosegura/date_assistant/badge.svg?branch=main)](https://coveralls.io/github/jalvaradosegura/date_assistant?branch=main)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)\n[![basic-quality-check](https://github.com/jalvaradosegura/date_assistant/actions/workflows/code_quality.yml/badge.svg)](https://github.com/jalvaradosegura/date_assistant/actions/workflows/code_quality.yml)\n[![GitHub license](https://img.shields.io/github/license/jalvaradosegura/date_assistant)](https://github.com/jalvaradosegura/date_assistant/blob/main/LICENSE)\n[![Downloads](https://pepy.tech/badge/date-assistant)](https://pepy.tech/project/date-assistant)\n[![Documentation Status](https://readthedocs.org/projects/date-assistant/badge/?version=latest)](https://date-assistant.readthedocs.io)\n\n# Date Assistant\nFor more details take a look at the [docs](https://date-assistant.readthedocs.io)\n\n## Installation\ndate-assistant is published on [PyPI](https://pypi.org/project/date-assistant/) and can be installed from there:\n```\npip install date-assistant\n```\n\n## Usage\n> 💡 Please consider that the default date format is '%Y-%m-%d'. Anyways, you can indicate the format of your date if you need to.\n\n### Functions approach\n\n#### Get the difference of days, months or years between 2 dates\n```py\nfrom date_assistant import (\n    get_days_diff_between,\n    get_months_diff_between,\n    get_years_diff_between,\n)\nfrom date_assistant.formats import DD_MM_YYYY, YYYY_MM\n\n\nget_days_diff_between('2021-01-01', '2021-01-11')\n# 10\nget_days_diff_between('2021-01-01', '21-01-2021', date2_format=DD_MM_YYYY)\n# 20\n\nget_months_diff_between('2021-01-01', '2022-01-11')\n# 12\nget_months_diff_between('2021-01-05', '2021-02-01')\n# 0\nget_months_diff_between('2021-01', '2021-02-21', date1_format=YYYY_MM)\n# 1\n\nget_years_diff_between('2021-01-01', '2022-01-11')\n# 1\nget_years_diff_between('2021-01-05', '2022-01-01')\n# 0\nget_years_diff_between('2021-01', '2023-01-01', date1_format=YYYY_MM)\n# 2\n```\n> 💡 See how months and years are only counted if a full year or month has passed.\n\n#### Get the amount of years or months started between 2 dates\n```py\nfrom date_assistant import (\n    get_months_started_between,\n    get_years_started_between,\n)\nfrom date_assistant.formats import YYYY_MM\n\n\nget_months_started_between('2021-01-05', '2021-02-01')\n# 1\nget_months_started_between('2021-01-01', '2022-01-11')\n# 12\nget_months_started_between('2021-01', '2021-02-21', date1_format=YYYY_MM)\n# 1\n\nget_years_started_between('2021-01-01', '2020-12-31')\n# 1\nget_years_started_between('2021-01-05', '2022-01-01')\n# 1\nget_years_started_between('2021-01', '2023-01-01', date1_format=YYYY_MM)\n# 2\n```\n\n> 💡 In contrast with the previous block example, here you don't need a full year or month between dates to count. If a new year or month started, it count.\n\n### Classes approach\n\n#### Get the difference of days, months or years between 2 dates\n```py\nfrom date_assistant import DateAssistant\n\nmy_birthday_2021 = DateAssistant('2021-07-13')\ndate_assistant_birthday = '2021-08-18'\n\nmy_birthday_2021.days_diff_with(date_assistant_birthday)\n# 36\nmy_birthday_2021.months_diff_with(date_assistant_birthday)\n# 1\nmy_birthday_2021.years_diff_with(date_assistant_birthday)\n# 0\n```\n\n#### Get the amount of years or months started since or until some date\n```py\nfrom date_assistant import DateAssistant\n\nlast_day_of_2021 = DateAssistant('2021-12-31')\nfirst_day_of_2022 = '2022-01-01'\nfirst_day_of_2023 = '2023-01-01'\ndate_assistant_birthday = '2021-08-18'\n\nlast_day_of_2021.years_started_until(first_day_of_2022)\n# 1\nlast_day_of_2021.years_started_until(first_day_of_2023)\n# 2\nlast_day_of_2021.months_started_until(first_day_of_2022)\n# 1\nlast_day_of_2021.months_started_since(date_assistant_birthday)\n# 4\n```\n",
    'author': 'Jorge Alvarado',
    'author_email': 'alvaradosegurajorge@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jalvaradosegura/date-assistant',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
