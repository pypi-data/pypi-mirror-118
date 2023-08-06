# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['python_redis_orm']

package_data = \
{'': ['*']}

install_requires = \
['redis>=3.5.3,<4.0.0']

setup_kwargs = {
    'name': 'python-redis-orm',
    'version': '0.1.2',
    'description': 'Python Redis ORM, turns redis to a fully functional in-memory database, inspired by Django ORM',
    'long_description': "# redis-orm\n\n## **Python Redis ORM, turns redis to a fully functional in-memory database, inspired by Django ORM**\n\nFor one project, I needed to work with redis, but redis-py provides a minimum level of work with redis. I didn't find any Django-like ORM for redis, so I wrote this library, then there will be a port to Django.\n\n### Working with this library, you are expected:\n\n- Fully works in 2021\n- Django-like architecture\n- Easy adaptation to your needs\n- Adequate informational messages and error messages\n- Built-in RedisModel class\n- 6 built-in types of fields:\n    - RedisField - base class for nesting\n    - RedisString - string\n    - RedisNumber - int or float\n    - RedisId - instances IDs\n    - RedisDatetime - for work with date and time, via python datetime\n    - RedisForeignKey - for links to other redis models\n- All fields supports:\n    - Automatically serialization and deserialization\n    - TTL (Time To Live)\n    - Default values\n    - Providing functions to default values\n    - Allow null values setting\n    - Choices\n- Extras:\n    - Ignore deserialization errors setting - do not raise errors, while deserealizing data\n    - Save consistency setting - show structure-first data\n\n\n# Installation\n`pip install redis-orm`\n\n[Here is PyPi](https://pypi.org/project/redis-orm/)\n\n\n# Usage\n",
    'author': 'Anton Nechaev',
    'author_email': 'antonnechaev990@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gh0st-work/python_redis_orm',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
