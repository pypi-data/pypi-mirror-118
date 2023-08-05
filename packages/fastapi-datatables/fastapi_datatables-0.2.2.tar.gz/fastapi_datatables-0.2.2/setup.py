# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_datatables']

package_data = \
{'': ['*'],
 'fastapi_datatables': ['.mypy_cache/*',
                        '.mypy_cache/3.9/*',
                        '.mypy_cache/3.9/_typeshed/*',
                        '.mypy_cache/3.9/aiofiles/*',
                        '.mypy_cache/3.9/aiofiles/threadpool/*',
                        '.mypy_cache/3.9/asyncio/*',
                        '.mypy_cache/3.9/collections/*',
                        '.mypy_cache/3.9/concurrent/*',
                        '.mypy_cache/3.9/concurrent/futures/*',
                        '.mypy_cache/3.9/ctypes/*',
                        '.mypy_cache/3.9/dotenv/*',
                        '.mypy_cache/3.9/email/*',
                        '.mypy_cache/3.9/fastapi/*',
                        '.mypy_cache/3.9/fastapi/dependencies/*',
                        '.mypy_cache/3.9/fastapi/openapi/*',
                        '.mypy_cache/3.9/fastapi/security/*',
                        '.mypy_cache/3.9/fastapi_datatables/*',
                        '.mypy_cache/3.9/html/*',
                        '.mypy_cache/3.9/http/*',
                        '.mypy_cache/3.9/importlib/*',
                        '.mypy_cache/3.9/json/*',
                        '.mypy_cache/3.9/logging/*',
                        '.mypy_cache/3.9/multiprocessing/*',
                        '.mypy_cache/3.9/os/*',
                        '.mypy_cache/3.9/pydantic/*',
                        '.mypy_cache/3.9/sqlalchemy/*',
                        '.mypy_cache/3.9/sqlalchemy/connectors/*',
                        '.mypy_cache/3.9/sqlalchemy/databases/*',
                        '.mypy_cache/3.9/sqlalchemy/dialects/*',
                        '.mypy_cache/3.9/sqlalchemy/dialects/firebird/*',
                        '.mypy_cache/3.9/sqlalchemy/dialects/mssql/*',
                        '.mypy_cache/3.9/sqlalchemy/dialects/mysql/*',
                        '.mypy_cache/3.9/sqlalchemy/dialects/oracle/*',
                        '.mypy_cache/3.9/sqlalchemy/dialects/postgresql/*',
                        '.mypy_cache/3.9/sqlalchemy/dialects/sqlite/*',
                        '.mypy_cache/3.9/sqlalchemy/dialects/sybase/*',
                        '.mypy_cache/3.9/sqlalchemy/engine/*',
                        '.mypy_cache/3.9/sqlalchemy/event/*',
                        '.mypy_cache/3.9/sqlalchemy/ext/*',
                        '.mypy_cache/3.9/sqlalchemy/ext/declarative/*',
                        '.mypy_cache/3.9/sqlalchemy/orm/*',
                        '.mypy_cache/3.9/sqlalchemy/sql/*',
                        '.mypy_cache/3.9/sqlalchemy/util/*',
                        '.mypy_cache/3.9/starlette/*',
                        '.mypy_cache/3.9/starlette/middleware/*',
                        '.mypy_cache/3.9/urllib/*']}

install_requires = \
['SQLAlchemy==1.3.23',
 'fastapi>=0.68.0,<0.69.0',
 'sqlalchemy-filters>=0.12.0,<0.13.0']

setup_kwargs = {
    'name': 'fastapi-datatables',
    'version': '0.2.2',
    'description': 'A library, that makes using SQLAlchemy tables with FastAPI easy. It implements filtration, pagination, ordering and text search out of the box. With utilization of FastAPI\'s "Depends" makes it easy to get filtration data from query parameters.',
    'long_description': None,
    'author': 'LeaveMyYard',
    'author_email': 'zhukovpavel2001@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
